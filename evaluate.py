import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch

from flow_sampling import (
    euler_sample,
    guided_euler_sample,
    load_model_from_checkpoint,
    load_real_data,
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
    "guidance_decay": "constant",
    "max_guidance_norm": 10.0,
}

DEFAULT_SCENARIOS = (
    {
        "name": "in_distribution_origin",
        "obstacle_center": (0.0, 0.0, 0.0),
        "obstacle_radius": 1.0,
    },
    {
        "name": "ood_shifted_y",
        "obstacle_center": (0.0, 1.5, 0.0),
        "obstacle_radius": 1.0,
    },
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Batch evaluation for baseline and energy-guided Rectified Flow."
    )
    parser.add_argument("--data-path", type=str, default=STANDARD_EXPERIMENT["data_path"])
    parser.add_argument("--checkpoint-path", type=str, default=STANDARD_EXPERIMENT["checkpoint_path"])
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
        default=STANDARD_EXPERIMENT["guidance_decay"],
        choices=["constant", "linear"],
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
    parser.add_argument("--output-json", type=str, default="outputs/evaluation_results.json")
    parser.add_argument("--output-markdown", type=str, default="outputs/evaluation_summary.md")
    return parser.parse_args()


def resolve_device(device_arg: str) -> torch.device:
    from model import get_default_device

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
    obstacle_center: np.ndarray,
    obstacle_radius: float,
) -> dict[str, float]:
    collision_rate, success_rate, min_distance = obstacle_distance_stats(
        trajectories=trajectories,
        obstacle_center=obstacle_center,
        obstacle_radius=obstacle_radius,
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
                "obstacle_center": (float(cx), float(cy), float(cz)),
                "obstacle_radius": float(radius),
            }
        )
    return scenarios


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
    obstacle_center: np.ndarray,
    obstacle_radius: float,
    guidance_scale: float,
    guidance_margin: float,
    guidance_decay: str,
    max_guidance_norm: float,
) -> tuple[np.ndarray, float]:
    obstacle_center_tensor = torch.tensor(obstacle_center, device=device, dtype=torch.float32)
    synchronize_if_needed(device)
    start = time.perf_counter()
    generated = guided_euler_sample(
        model=model,
        num_samples=num_samples,
        seq_len=seq_len,
        point_dim=point_dim,
        steps=steps,
        device=device,
        obstacle_center=obstacle_center_tensor,
        obstacle_radius=obstacle_radius,
        guidance_scale=guidance_scale,
        guidance_margin=guidance_margin,
        guidance_decay=guidance_decay,
        max_guidance_norm=max_guidance_norm,
        z_init=z_init,
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
        for method in ("baseline", "guided"):
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
    lines.extend(
        [
            "",
            "## Reading The Table",
            "",
            "- `success_rate` is the primary obstacle-avoidance metric.",
            "- `smoothness` is the mean squared second difference; lower is smoother.",
            "- Baseline and guided use the same checkpoint, seed, sample count, integration steps, and initial noise z0.",
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

    model = load_model_from_checkpoint(
        checkpoint_path=Path(args.checkpoint_path),
        seq_len=seq_len,
        point_dim=point_dim,
        device=device,
    )

    results: dict[str, object] = {
        "config": {
            "data_path": args.data_path,
            "checkpoint_path": args.checkpoint_path,
            "device": str(device),
            "num_samples": num_samples,
            "steps": int(args.steps),
            "seed": int(args.seed),
            "guidance_scale": float(args.guidance_scale),
            "guidance_margin": float(args.guidance_margin),
            "guidance_decay": args.guidance_decay,
            "max_guidance_norm": float(args.max_guidance_norm),
        },
        "scenarios": [],
    }

    for scenario in scenarios:
        obstacle_center = np.asarray(scenario["obstacle_center"], dtype=np.float32)
        obstacle_radius = float(scenario["obstacle_radius"])

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
        guided, guided_time = sample_guided(
            model=model,
            num_samples=num_samples,
            seq_len=seq_len,
            point_dim=point_dim,
            steps=int(args.steps),
            device=device,
            z_init=z_init.clone(),
            obstacle_center=obstacle_center,
            obstacle_radius=obstacle_radius,
            guidance_scale=float(args.guidance_scale),
            guidance_margin=float(args.guidance_margin),
            guidance_decay=str(args.guidance_decay),
            max_guidance_norm=float(args.max_guidance_norm),
        )

        baseline_metrics = evaluate_trajectories(baseline, obstacle_center, obstacle_radius)
        guided_metrics = evaluate_trajectories(guided, obstacle_center, obstacle_radius)
        baseline_metrics["inference_time_seconds"] = baseline_time
        guided_metrics["inference_time_seconds"] = guided_time

        results["scenarios"].append(
            {
                "name": str(scenario["name"]),
                "obstacle_center": obstacle_center.tolist(),
                "obstacle_radius": obstacle_radius,
                "baseline": baseline_metrics,
                "guided": guided_metrics,
            }
        )

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
