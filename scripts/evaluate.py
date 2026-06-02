import _bootstrap  # noqa: E402, F401 — must precede rectified_flow imports

import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch

from rectified_flow.sampling import (
    conditional_euler_sample,
    conditional_guided_euler_sample,
    euler_sample,
    guided_euler_sample,
    load_conditional_model_from_checkpoint,
    load_model_from_checkpoint,
    load_real_data,
    make_obstacle_condition,
    make_initial_noise,
    obstacle_distance_stats,
    set_seed,
)


STANDARD_EXPERIMENT = {
    "data_path": "dataset/toy_trajectories.npy",
    "checkpoint_path": "checkpoints/rectified_flow_mlp.pt",
    "num_samples": 200,
    "steps": 20,
    "seed": 42,
    "guidance_scale": 3.0,
    "guidance_margin": 2.0,
    "guidance_decays": ("constant", "distance_gated"),
    "max_guidance_norm": 10.0,
}

DEFAULT_SCENARIOS = (
    {
        "name": "in_distribution_origin",
        "obstacles": [((0.0, 0.0, 0.0), 1.0)],
    },
    {
        "name": "ood_shifted_y",
        "obstacles": [((0.0, 1.5, 0.0), 1.0)],
    },
    {
        "name": "ood_double_gap",
        "obstacles": [((0.0, 1.5, 0.0), 1.0), ((0.0, -1.5, 0.0), 1.0)],
    },
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Batch evaluation for baseline and energy-guided Rectified Flow."
    )
    parser.add_argument("--data-path", type=str, default=STANDARD_EXPERIMENT["data_path"])
    parser.add_argument("--checkpoint-path", type=str, default=STANDARD_EXPERIMENT["checkpoint_path"])
    parser.add_argument(
        "--conditional-checkpoint-path",
        type=str,
        default="",
        help=(
            "Optional conditional checkpoint. When provided, evaluate conditional "
            "and conditional+guided methods alongside the unconditional model."
        ),
    )
    parser.add_argument("--num-samples", type=int, default=STANDARD_EXPERIMENT["num_samples"])
    parser.add_argument("--steps", type=int, default=STANDARD_EXPERIMENT["steps"])
    parser.add_argument("--seed", type=int, default=STANDARD_EXPERIMENT["seed"])
    parser.add_argument(
        "--device",
        type=str,
        default="auto",
        choices=["auto", "cpu", "cuda", "mps"],
        help="Evaluation device. auto = cuda -> mps -> cpu",
    )
    parser.add_argument("--guidance-scale", type=float, default=STANDARD_EXPERIMENT["guidance_scale"])
    parser.add_argument("--guidance-margin", type=float, default=STANDARD_EXPERIMENT["guidance_margin"])
    parser.add_argument(
        "--guidance-decay",
        type=str,
        action="append",
        choices=["constant", "distance_gated"],
        help=(
            "Guidance mode to evaluate. Can be repeated. "
            "Defaults to constant and distance_gated."
        ),
    )
    parser.add_argument("--max-guidance-norm", type=float, default=STANDARD_EXPERIMENT["max_guidance_norm"])
    parser.add_argument(
        "--scenario",
        action="append",
        nargs=5,
        metavar=("NAME", "CX", "CY", "CZ", "R"),
        help=(
            "Optional scenario override. Can be repeated. "
            "Example: --scenario shifted 0 1.5 0 1"
        ),
    )
    parser.add_argument(
        "--random-ood-count",
        type=int,
        default=0,
        help="Number of random single-obstacle OOD scenarios to append.",
    )
    parser.add_argument(
        "--random-ood-y-range",
        type=float,
        nargs=2,
        default=(-2.5, 2.5),
        metavar=("MIN", "MAX"),
        help="Sampling range for random obstacle y coordinates.",
    )
    parser.add_argument(
        "--random-ood-z-range",
        type=float,
        nargs=2,
        default=(-1.5, 1.5),
        metavar=("MIN", "MAX"),
        help="Sampling range for random obstacle z coordinates.",
    )
    parser.add_argument(
        "--random-ood-radius-range",
        type=float,
        nargs=2,
        default=(0.8, 1.2),
        metavar=("MIN", "MAX"),
        help="Sampling range for random obstacle radii.",
    )
    parser.add_argument(
        "--random-ood-min-center-norm",
        type=float,
        default=1.0,
        help="Reject random obstacle centers closer than this distance to the training obstacle center.",
    )
    parser.add_argument("--output-json", type=str, default="outputs/evaluation_results.json")
    parser.add_argument("--output-markdown", type=str, default="outputs/evaluation_summary.md")
    return parser.parse_args()


def resolve_device(device_arg: str) -> torch.device:
    from rectified_flow.model import get_default_device

    if device_arg == "auto":
        return get_default_device()
    if device_arg == "cuda":
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA is not available but --device=cuda was requested.")
        return torch.device("cuda")
    if device_arg == "mps":
        if not torch.backends.mps.is_available():
            raise RuntimeError("MPS is not available but --device=mps was requested.")
        return torch.device("mps")
    return torch.device("cpu")


def synchronize_if_needed(device: torch.device) -> None:
    if device.type == "cuda":
        torch.cuda.synchronize(device)


def trajectory_smoothness(trajectories: np.ndarray) -> float:
    if trajectories.shape[1] < 3:
        return 0.0
    second_diff = trajectories[:, 2:, :] - 2.0 * trajectories[:, 1:-1, :] + trajectories[:, :-2, :]
    return float(np.mean(np.linalg.norm(second_diff, axis=-1) ** 2))


def trajectory_path_length(trajectories: np.ndarray) -> float:
    if trajectories.shape[1] < 2:
        return 0.0
    segment_lengths = np.linalg.norm(np.diff(trajectories, axis=1), axis=-1)
    return float(np.mean(np.sum(segment_lengths, axis=1)))


def evaluate_trajectories(
    trajectories: np.ndarray,
    obstacle_centers: np.ndarray,
    obstacle_radii: np.ndarray,
) -> dict[str, float]:
    collision_rate, success_rate, min_distance = obstacle_distance_stats(
        trajectories=trajectories,
        obstacle_center=obstacle_centers,
        obstacle_radius=obstacle_radii,
    )
    return {
        "collision_rate": collision_rate,
        "success_rate": success_rate,
        "min_distance_to_obstacle": min_distance,
        "smoothness": trajectory_smoothness(trajectories),
        "path_length": trajectory_path_length(trajectories),
    }


def parse_scenarios(raw_scenarios: list[list[str]] | None) -> list[dict[str, object]]:
    if not raw_scenarios:
        return [dict(scenario) for scenario in DEFAULT_SCENARIOS]

    scenarios = []
    for name, cx, cy, cz, radius in raw_scenarios:
        scenarios.append(
            {
                "name": name,
                "obstacles": [((float(cx), float(cy), float(cz)), float(radius))],
            }
        )
    return scenarios


def validate_range(name: str, values: tuple[float, float] | list[float]) -> tuple[float, float]:
    lower, upper = float(values[0]), float(values[1])
    if lower > upper:
        raise ValueError(f"{name} lower bound must be <= upper bound.")
    return lower, upper


def generate_random_ood_scenarios(
    count: int,
    seed: int,
    y_range: tuple[float, float] | list[float],
    z_range: tuple[float, float] | list[float],
    radius_range: tuple[float, float] | list[float],
    min_center_norm: float,
) -> list[dict[str, object]]:
    if count < 0:
        raise ValueError("random_ood_count must be non-negative.")
    if count == 0:
        return []
    y_min, y_max = validate_range("random_ood_y_range", y_range)
    z_min, z_max = validate_range("random_ood_z_range", z_range)
    r_min, r_max = validate_range("random_ood_radius_range", radius_range)
    if r_min < 0.0:
        raise ValueError("random obstacle radii must be non-negative.")
    if min_center_norm < 0.0:
        raise ValueError("random_ood_min_center_norm must be non-negative.")

    rng = np.random.default_rng(seed)
    scenarios = []
    attempts = 0
    max_attempts = max(1000, count * 100)
    while len(scenarios) < count and attempts < max_attempts:
        attempts += 1
        center = np.array(
            [
                0.0,
                rng.uniform(y_min, y_max),
                rng.uniform(z_min, z_max),
            ],
            dtype=np.float32,
        )
        if np.linalg.norm(center) < min_center_norm:
            continue
        radius = float(rng.uniform(r_min, r_max))
        scenarios.append(
            {
                "name": f"random_ood_{len(scenarios):03d}",
                "obstacles": [(tuple(float(v) for v in center), radius)],
                "random_ood": True,
            }
        )
    if len(scenarios) != count:
        raise RuntimeError(
            f"Only sampled {len(scenarios)} random OOD scenarios after {max_attempts} attempts."
        )
    return scenarios


def unpack_obstacles(scenario: dict[str, object]) -> tuple[np.ndarray, np.ndarray]:
    obstacles = scenario.get("obstacles")
    if obstacles is None:
        center = scenario["obstacle_center"]
        radius = scenario["obstacle_radius"]
        return (
            np.asarray(center, dtype=np.float32).reshape(1, 3),
            np.asarray([radius], dtype=np.float32),
        )

    centers = []
    radii = []
    for center, radius in obstacles:
        centers.append(center)
        radii.append(radius)
    return np.asarray(centers, dtype=np.float32), np.asarray(radii, dtype=np.float32)


def sample_baseline(
    model: torch.nn.Module,
    num_samples: int,
    seq_len: int,
    point_dim: int,
    steps: int,
    device: torch.device,
    z_init: torch.Tensor,
) -> tuple[np.ndarray, float]:
    synchronize_if_needed(device)
    start = time.perf_counter()
    generated = euler_sample(
        model=model,
        num_samples=num_samples,
        seq_len=seq_len,
        point_dim=point_dim,
        steps=steps,
        device=device,
        z_init=z_init,
    )
    synchronize_if_needed(device)
    elapsed = time.perf_counter() - start
    return generated.detach().cpu().numpy().astype(np.float32), elapsed


def sample_guided(
    model: torch.nn.Module,
    num_samples: int,
    seq_len: int,
    point_dim: int,
    steps: int,
    device: torch.device,
    z_init: torch.Tensor,
    obstacle_centers: np.ndarray,
    obstacle_radii: np.ndarray,
    guidance_scale: float,
    guidance_margin: float,
    guidance_decay: str,
    max_guidance_norm: float,
) -> tuple[np.ndarray, float]:
    obstacle_centers_tensor = torch.tensor(obstacle_centers, device=device, dtype=torch.float32)
    obstacle_radii_tensor = torch.tensor(obstacle_radii, device=device, dtype=torch.float32)
    synchronize_if_needed(device)
    start = time.perf_counter()
    generated = guided_euler_sample(
        model=model,
        num_samples=num_samples,
        seq_len=seq_len,
        point_dim=point_dim,
        steps=steps,
        device=device,
        obstacle_center=obstacle_centers_tensor[0],
        obstacle_radius=float(obstacle_radii_tensor[0].item()),
        guidance_scale=guidance_scale,
        guidance_margin=guidance_margin,
        guidance_decay=guidance_decay,
        max_guidance_norm=max_guidance_norm,
        z_init=z_init,
        obstacle_centers=obstacle_centers_tensor,
        obstacle_radii=obstacle_radii_tensor,
    )
    synchronize_if_needed(device)
    elapsed = time.perf_counter() - start
    return generated.detach().cpu().numpy().astype(np.float32), elapsed


def sample_conditional(
    model: torch.nn.Module,
    condition: torch.Tensor,
    num_samples: int,
    seq_len: int,
    point_dim: int,
    steps: int,
    device: torch.device,
    z_init: torch.Tensor,
) -> tuple[np.ndarray, float]:
    synchronize_if_needed(device)
    start = time.perf_counter()
    generated = conditional_euler_sample(
        model=model,
        condition=condition,
        num_samples=num_samples,
        seq_len=seq_len,
        point_dim=point_dim,
        steps=steps,
        device=device,
        z_init=z_init,
    )
    synchronize_if_needed(device)
    elapsed = time.perf_counter() - start
    return generated.detach().cpu().numpy().astype(np.float32), elapsed


def sample_conditional_guided(
    model: torch.nn.Module,
    condition: torch.Tensor,
    num_samples: int,
    seq_len: int,
    point_dim: int,
    steps: int,
    device: torch.device,
    z_init: torch.Tensor,
    obstacle_centers: np.ndarray,
    obstacle_radii: np.ndarray,
    guidance_scale: float,
    guidance_margin: float,
    guidance_decay: str,
    max_guidance_norm: float,
) -> tuple[np.ndarray, float]:
    obstacle_centers_tensor = torch.tensor(obstacle_centers, device=device, dtype=torch.float32)
    obstacle_radii_tensor = torch.tensor(obstacle_radii, device=device, dtype=torch.float32)
    synchronize_if_needed(device)
    start = time.perf_counter()
    generated = conditional_guided_euler_sample(
        model=model,
        condition=condition,
        num_samples=num_samples,
        seq_len=seq_len,
        point_dim=point_dim,
        steps=steps,
        device=device,
        obstacle_center=obstacle_centers_tensor[0],
        obstacle_radius=float(obstacle_radii_tensor[0].item()),
        guidance_scale=guidance_scale,
        guidance_margin=guidance_margin,
        guidance_decay=guidance_decay,
        max_guidance_norm=max_guidance_norm,
        z_init=z_init,
        obstacle_centers=obstacle_centers_tensor,
        obstacle_radii=obstacle_radii_tensor,
    )
    synchronize_if_needed(device)
    elapsed = time.perf_counter() - start
    return generated.detach().cpu().numpy().astype(np.float32), elapsed


def format_markdown(results: dict[str, object]) -> str:
    lines = [
        "# Evaluation Summary",
        "",
        "## Standard Experiment",
        "",
    ]
    for key, value in results["config"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Results", ""])
    lines.append("| Scenario | Method | Success Rate | Collision Rate | Min Distance | Smoothness | Path Length | Time (s) |")
    lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for scenario in results["scenarios"]:
        for method in scenario["methods"]:
            metrics = scenario[method]
            lines.append(
                "| {scenario} | {method} | {success:.4f} | {collision:.4f} | {min_dist:.4f} | "
                "{smoothness:.4f} | {path_length:.4f} | {time:.4f} |".format(
                    scenario=scenario["name"],
                    method=method,
                    success=metrics["success_rate"],
                    collision=metrics["collision_rate"],
                    min_dist=metrics["min_distance_to_obstacle"],
                    smoothness=metrics["smoothness"],
                    path_length=metrics["path_length"],
                    time=metrics["inference_time_seconds"],
                )
            )
        if "conditional_skipped_reason" in scenario:
            lines.append(
                "| {scenario} | conditional_skipped | - | - | - | - | - | - |".format(
                    scenario=scenario["name"]
                )
            )
    random_summary = results.get("random_ood_summary", {})
    if random_summary:
        lines.extend(["", "## Random OOD Summary", ""])
        lines.append("| Method | Success Rate | Collision Rate | Min Distance | Smoothness | Path Length | Time (s) |")
        lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
        for method, metrics in random_summary.items():
            lines.append(
                "| {method} | {success:.4f} | {collision:.4f} | {min_dist:.4f} | "
                "{smoothness:.4f} | {path_length:.4f} | {time:.4f} |".format(
                    method=method,
                    success=metrics["success_rate"],
                    collision=metrics["collision_rate"],
                    min_dist=metrics["min_distance_to_obstacle"],
                    smoothness=metrics["smoothness"],
                    path_length=metrics["path_length"],
                    time=metrics["inference_time_seconds"],
                )
            )
    lines.extend(
        [
            "",
            "## Reading The Table",
            "",
            "- `success_rate` is the primary obstacle-avoidance metric.",
            "- `smoothness` is the mean squared second difference; lower is smoother.",
            "- Unconditional and conditional methods use paired initial noise z0 within each scenario.",
            "- Conditional methods require a conditional checkpoint and encode obstacles as flattened `(cx, cy, cz, radius)` slots.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    device = resolve_device(args.device)
    real_all = load_real_data(Path(args.data_path))
    seq_len = int(real_all.shape[1])
    point_dim = int(real_all.shape[2])
    num_samples = min(int(args.num_samples), int(real_all.shape[0]))
    scenarios = parse_scenarios(args.scenario)
    random_scenarios = generate_random_ood_scenarios(
        count=int(args.random_ood_count),
        seed=int(args.seed) + 10_000,
        y_range=args.random_ood_y_range,
        z_range=args.random_ood_z_range,
        radius_range=args.random_ood_radius_range,
        min_center_norm=float(args.random_ood_min_center_norm),
    )
    scenarios.extend(random_scenarios)
    guidance_decays = tuple(args.guidance_decay or STANDARD_EXPERIMENT["guidance_decays"])

    model = load_model_from_checkpoint(
        checkpoint_path=Path(args.checkpoint_path),
        seq_len=seq_len,
        point_dim=point_dim,
        device=device,
    )
    conditional_model = None
    conditional_condition_dim = 0
    if args.conditional_checkpoint_path:
        conditional_model = load_conditional_model_from_checkpoint(
            checkpoint_path=Path(args.conditional_checkpoint_path),
            seq_len=seq_len,
            point_dim=point_dim,
            device=device,
        )
        conditional_condition_dim = int(getattr(conditional_model, "condition_dim"))

    results: dict[str, object] = {
        "config": {
            "data_path": args.data_path,
            "checkpoint_path": args.checkpoint_path,
            "conditional_checkpoint_path": args.conditional_checkpoint_path,
            "conditional_condition_dim": conditional_condition_dim,
            "device": str(device),
            "num_samples": num_samples,
            "steps": int(args.steps),
            "seed": int(args.seed),
            "guidance_scale": float(args.guidance_scale),
            "guidance_margin": float(args.guidance_margin),
            "guidance_decays": list(guidance_decays),
            "max_guidance_norm": float(args.max_guidance_norm),
            "random_ood_count": int(args.random_ood_count),
            "random_ood_y_range": [float(v) for v in args.random_ood_y_range],
            "random_ood_z_range": [float(v) for v in args.random_ood_z_range],
            "random_ood_radius_range": [float(v) for v in args.random_ood_radius_range],
            "random_ood_min_center_norm": float(args.random_ood_min_center_norm),
        },
        "scenarios": [],
    }

    for scenario in scenarios:
        obstacle_centers, obstacle_radii = unpack_obstacles(scenario)

        set_seed(int(args.seed))
        z_init = make_initial_noise(num_samples, seq_len, point_dim, device)

        baseline, baseline_time = sample_baseline(
            model=model,
            num_samples=num_samples,
            seq_len=seq_len,
            point_dim=point_dim,
            steps=int(args.steps),
            device=device,
            z_init=z_init,
        )
        baseline_metrics = evaluate_trajectories(baseline, obstacle_centers, obstacle_radii)
        baseline_metrics["inference_time_seconds"] = baseline_time

        scenario_result: dict[str, object] = {
            "name": str(scenario["name"]),
            "obstacles": [
                {
                    "center": center.tolist(),
                    "radius": float(radius),
                }
                for center, radius in zip(obstacle_centers, obstacle_radii)
            ],
            "methods": ["baseline"],
            "baseline": baseline_metrics,
        }

        for guidance_decay in guidance_decays:
            guided, guided_time = sample_guided(
                model=model,
                num_samples=num_samples,
                seq_len=seq_len,
                point_dim=point_dim,
                steps=int(args.steps),
                device=device,
                z_init=z_init.clone(),
                obstacle_centers=obstacle_centers,
                obstacle_radii=obstacle_radii,
                guidance_scale=float(args.guidance_scale),
                guidance_margin=float(args.guidance_margin),
                guidance_decay=str(guidance_decay),
                max_guidance_norm=float(args.max_guidance_norm),
            )
            guided_metrics = evaluate_trajectories(guided, obstacle_centers, obstacle_radii)
            guided_metrics["inference_time_seconds"] = guided_time
            method_name = f"guided_{guidance_decay}"
            scenario_result["methods"].append(method_name)
            scenario_result[method_name] = guided_metrics

        if conditional_model is not None:
            try:
                condition = make_obstacle_condition(
                    obstacle_centers=torch.tensor(obstacle_centers, device=device, dtype=torch.float32),
                    obstacle_radii=torch.tensor(obstacle_radii, device=device, dtype=torch.float32),
                    condition_dim=conditional_condition_dim,
                )
            except ValueError as exc:
                scenario_result["conditional_skipped_reason"] = str(exc)
            else:
                conditional, conditional_time = sample_conditional(
                    model=conditional_model,
                    condition=condition,
                    num_samples=num_samples,
                    seq_len=seq_len,
                    point_dim=point_dim,
                    steps=int(args.steps),
                    device=device,
                    z_init=z_init.clone(),
                )
                conditional_metrics = evaluate_trajectories(
                    conditional, obstacle_centers, obstacle_radii
                )
                conditional_metrics["inference_time_seconds"] = conditional_time
                scenario_result["methods"].append("conditional")
                scenario_result["conditional"] = conditional_metrics

                for guidance_decay in guidance_decays:
                    conditional_guided, conditional_guided_time = sample_conditional_guided(
                        model=conditional_model,
                        condition=condition,
                        num_samples=num_samples,
                        seq_len=seq_len,
                        point_dim=point_dim,
                        steps=int(args.steps),
                        device=device,
                        z_init=z_init.clone(),
                        obstacle_centers=obstacle_centers,
                        obstacle_radii=obstacle_radii,
                        guidance_scale=float(args.guidance_scale),
                        guidance_margin=float(args.guidance_margin),
                        guidance_decay=str(guidance_decay),
                        max_guidance_norm=float(args.max_guidance_norm),
                    )
                    conditional_guided_metrics = evaluate_trajectories(
                        conditional_guided, obstacle_centers, obstacle_radii
                    )
                    conditional_guided_metrics["inference_time_seconds"] = conditional_guided_time
                    method_name = f"conditional_guided_{guidance_decay}"
                    scenario_result["methods"].append(method_name)
                    scenario_result[method_name] = conditional_guided_metrics

        results["scenarios"].append(scenario_result)

    if random_scenarios:
        random_names = {str(scenario["name"]) for scenario in random_scenarios}
        methods = results["scenarios"][0]["methods"] if results["scenarios"] else []
        random_summary: dict[str, dict[str, float]] = {}
        random_results = [
            scenario
            for scenario in results["scenarios"]
            if str(scenario["name"]) in random_names
        ]
        for method in methods:
            method_metrics = [scenario[method] for scenario in random_results]
            random_summary[method] = {
                key: float(np.mean([metrics[key] for metrics in method_metrics]))
                for key in (
                    "collision_rate",
                    "success_rate",
                    "min_distance_to_obstacle",
                    "smoothness",
                    "path_length",
                    "inference_time_seconds",
                )
            }
        results["random_ood_summary"] = random_summary

    json_path = Path(args.output_json)
    markdown_path = Path(args.output_markdown)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    markdown_path.write_text(format_markdown(results), encoding="utf-8")

    print(format_markdown(results))
    print(f"Saved JSON results: {json_path}")
    print(f"Saved Markdown summary: {markdown_path}")


if __name__ == "__main__":
    main()
