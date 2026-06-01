import argparse
import csv
import json
from pathlib import Path

import numpy as np
import torch

from evaluate import (
    evaluate_trajectories,
    generate_random_ood_scenarios,
    parse_scenarios,
    resolve_device,
    sample_baseline,
    sample_guided,
    unpack_obstacles,
)
from flow_sampling import load_model_from_checkpoint, load_real_data, make_initial_noise, set_seed


STANDARD_EXPERIMENT = {
    "data_path": "dataset/toy_trajectories.npy",
    "checkpoint_path": "checkpoints/rectified_flow_mlp.pt",
    "num_samples": 500,
    "steps": 20,
    "seed": 42,
    "guidance_scale": 3.0,
    "guidance_margin": 2.0,
    "guidance_decays": ("constant", "distance_gated"),
    "max_guidance_norm": 10.0,
}

DEFAULT_VALUES = {
    "guidance_scale": [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0],
    "guidance_margin": [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5],
    "max_guidance_norm": [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0, 8.0],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ablate energy guidance parameters across scenarios."
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
    parser.add_argument(
        "--ablate",
        type=str,
        default="all",
        choices=["all", "guidance_scale", "guidance_margin", "max_guidance_norm"],
        help="Which guidance parameter to sweep.",
    )
    parser.add_argument(
        "--values",
        type=float,
        nargs="+",
        help="Explicit sweep values. Defaults depend on the chosen --ablate.",
    )
    parser.add_argument("--guidance-scale", type=float, default=STANDARD_EXPERIMENT["guidance_scale"])
    parser.add_argument("--guidance-margin", type=float, default=STANDARD_EXPERIMENT["guidance_margin"])
    parser.add_argument(
        "--guidance-decay",
        type=str,
        action="append",
        choices=["constant", "distance_gated"],
        help="Guidance mode to evaluate. Can be repeated.",
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
    parser.add_argument(
        "--output-json",
        type=str,
        default="outputs/ablation_guidance_results.json",
    )
    parser.add_argument(
        "--output-markdown",
        type=str,
        default="outputs/ablation_guidance_summary.md",
    )
    parser.add_argument(
        "--output-csv",
        type=str,
        default="outputs/ablation_guidance_pareto.csv",
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        help="Save Pareto scatter plots from the sweep results.",
    )
    parser.add_argument(
        "--plot-dir",
        type=str,
        default="outputs/ablation_plots",
        help="Output directory for ablation plots.",
    )
    return parser.parse_args()


def format_markdown(results: dict[str, object]) -> str:
    lines = [
        "# Guidance Ablation Summary",
        "",
        "## Sweep Configuration",
        "",
    ]
    for key, value in results["config"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Results", ""])
    lines.append(
        "| Scenario | Decay | Param | Value | Success Rate | Collision Rate | Min Distance | Smoothness | Path Length | Time (s) |"
    )
    lines.append("| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for row in results["rows"]:
        lines.append(
            "| {scenario} | {decay} | {param} | {value:.4f} | {success:.4f} | {collision:.4f} | {min_dist:.4f} | "
            "{smoothness:.4f} | {path_length:.4f} | {time:.4f} |".format(
                scenario=row["scenario"],
                decay=row["guidance_decay"],
                param=row["param"],
                value=row["value"],
                success=row["success_rate"],
                collision=row["collision_rate"],
                min_dist=row["min_distance_to_obstacle"],
                smoothness=row["smoothness"],
                path_length=row["path_length"],
                time=row["inference_time_seconds"],
            )
        )

    summary = results.get("scenario_summary", {})
    if summary:
        lines.extend(["", "## Scenario Mean Summary", ""])
        lines.append(
            "| Scenario | Decay | Param | Value | Success Rate | Collision Rate | Min Distance | Smoothness | Path Length | Time (s) |"
        )
        lines.append("| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
        for row in summary.values():
            lines.append(
                "| {scenario} | {decay} | {param} | {value:.4f} | {success:.4f} | {collision:.4f} | {min_dist:.4f} | "
                "{smoothness:.4f} | {path_length:.4f} | {time:.4f} |".format(
                    scenario=row["scenario"],
                    decay=row["guidance_decay"],
                    param=row["param"],
                    value=row["value"],
                    success=row["success_rate"],
                    collision=row["collision_rate"],
                    min_dist=row["min_distance_to_obstacle"],
                    smoothness=row["smoothness"],
                    path_length=row["path_length"],
                    time=row["inference_time_seconds"],
                )
            )
    return "\n".join(lines) + "\n"


def summarize_rows(rows: list[dict[str, float]], key_fields: tuple[str, ...]) -> dict[str, dict[str, float]]:
    grouped: dict[str, list[dict[str, float]]] = {}
    for row in rows:
        key = "|".join(str(row[field]) for field in key_fields)
        grouped.setdefault(key, []).append(row)

    summary = {}
    for key, items in grouped.items():
        summary[key] = {
            "scenario": items[0]["scenario"],
            "guidance_decay": items[0]["guidance_decay"],
            "param": items[0]["param"],
            "value": items[0]["value"],
            "collision_rate": float(np.mean([item["collision_rate"] for item in items])),
            "success_rate": float(np.mean([item["success_rate"] for item in items])),
            "min_distance_to_obstacle": float(
                np.mean([item["min_distance_to_obstacle"] for item in items])
            ),
            "smoothness": float(np.mean([item["smoothness"] for item in items])),
            "path_length": float(np.mean([item["path_length"] for item in items])),
            "inference_time_seconds": float(np.mean([item["inference_time_seconds"] for item in items])),
        }
    return summary


def write_csv(rows: list[dict[str, float]], csv_path: Path) -> None:
    fieldnames = [
        "scenario",
        "guidance_decay",
        "param",
        "value",
        "success_rate",
        "collision_rate",
        "min_distance_to_obstacle",
        "smoothness",
        "path_length",
        "inference_time_seconds",
    ]
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in fieldnames})


def _safe_name(name: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "_-" else "_" for ch in name)


def plot_ablation(
    rows: list[dict[str, float]],
    sweep_param: str,
    output_dir: Path,
) -> list[Path]:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib is not available; skip plotting.")
        return []

    output_dir.mkdir(parents=True, exist_ok=True)
    scenarios = sorted({row["scenario"] for row in rows})
    output_paths: list[Path] = []

    for scenario in scenarios:
        scenario_rows = [row for row in rows if row["scenario"] == scenario]
        if not scenario_rows:
            continue

        decays = sorted({row["guidance_decay"] for row in scenario_rows})
        fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharex=True)
        ax_success, ax_smooth = axes

        for decay in decays:
            decay_rows = [row for row in scenario_rows if row["guidance_decay"] == decay]
            decay_rows = sorted(decay_rows, key=lambda item: item["value"])
            x_vals = [row["value"] for row in decay_rows]
            y_success = [row["success_rate"] for row in decay_rows]
            y_smooth = [row["smoothness"] for row in decay_rows]
            if decay == "baseline":
                ax_success.scatter(x_vals, y_success, label=decay, alpha=0.9, s=48, marker="X", color="black")
                ax_smooth.scatter(x_vals, y_smooth, label=decay, alpha=0.9, s=48, marker="X", color="black")
                continue
            ax_success.plot(x_vals, y_success, label=decay, alpha=0.85, linewidth=1.5)
            ax_success.scatter(x_vals, y_success, alpha=0.85, s=36)
            ax_smooth.plot(x_vals, y_smooth, label=decay, alpha=0.85, linewidth=1.5)
            ax_smooth.scatter(x_vals, y_smooth, alpha=0.85, s=36)

        ax_success.set_xlabel(sweep_param)
        ax_success.set_ylabel("success_rate")
        ax_success.set_title(f"Success | {scenario}")
        ax_success.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)

        ax_smooth.set_xlabel(sweep_param)
        ax_smooth.set_ylabel("smoothness")
        ax_smooth.set_title(f"Smoothness | {scenario}")
        ax_smooth.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)

        ax_success.legend(fontsize=8, frameon=False)
        fig.tight_layout()

        filename = f"ablation_{_safe_name(scenario)}_{_safe_name(sweep_param)}.png"
        output_path = output_dir / filename
        fig.savefig(output_path, dpi=160)
        plt.close(fig)
        output_paths.append(output_path)

    return output_paths


def _expand_output_path(base_path: Path, suffix: str, param: str) -> Path:
    if not suffix:
        return base_path
    stem = base_path.stem
    return base_path.with_name(f"{stem}_{param}{suffix}")


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
    if args.ablate == "all":
        sweep_params = ["guidance_scale", "guidance_margin", "max_guidance_norm"]
    else:
        sweep_params = [str(args.ablate)]

    model = load_model_from_checkpoint(
        checkpoint_path=Path(args.checkpoint_path),
        seq_len=seq_len,
        point_dim=point_dim,
        device=device,
    )

    json_path = Path(args.output_json)
    markdown_path = Path(args.output_markdown)
    csv_path = Path(args.output_csv)

    for sweep_param in sweep_params:
        sweep_values = list(args.values or DEFAULT_VALUES[sweep_param])
        sweep_values = [float(value) for value in sweep_values]

        if sweep_param == "guidance_margin":
            for value in sweep_values:
                if value < 0.0:
                    raise ValueError("guidance_margin values must be non-negative.")
        if sweep_param == "max_guidance_norm":
            for value in sweep_values:
                if value <= 0.0:
                    raise ValueError("max_guidance_norm values must be positive.")

        rows: list[dict[str, float]] = []

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
            rows.append(
                {
                    "scenario": str(scenario["name"]),
                    "guidance_decay": "baseline",
                    "param": sweep_param,
                    "value": 0.0,
                    **baseline_metrics,
                }
            )

            for guidance_decay in guidance_decays:
                for value in sweep_values:
                    guidance_scale = float(args.guidance_scale)
                    guidance_margin = float(args.guidance_margin)
                    max_guidance_norm = float(args.max_guidance_norm)
                    if sweep_param == "guidance_scale":
                        guidance_scale = value
                    elif sweep_param == "guidance_margin":
                        guidance_margin = value
                    elif sweep_param == "max_guidance_norm":
                        max_guidance_norm = value

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
                        guidance_scale=guidance_scale,
                        guidance_margin=guidance_margin,
                        guidance_decay=str(guidance_decay),
                        max_guidance_norm=max_guidance_norm,
                    )
                    guided_metrics = evaluate_trajectories(guided, obstacle_centers, obstacle_radii)
                    guided_metrics["inference_time_seconds"] = guided_time
                    rows.append(
                        {
                            "scenario": str(scenario["name"]),
                            "guidance_decay": str(guidance_decay),
                            "param": sweep_param,
                            "value": float(value),
                            **guided_metrics,
                        }
                    )

        scenario_summary = summarize_rows(
            rows=[row for row in rows if not row["scenario"].startswith("random_ood_")],
            key_fields=("scenario", "guidance_decay", "param", "value"),
        )

        random_summary = {}
        random_rows = [row for row in rows if row["scenario"].startswith("random_ood_")]
        if random_rows:
            random_summary = summarize_rows(
                rows=random_rows,
                key_fields=("guidance_decay", "param", "value"),
            )

        results = {
            "config": {
                "data_path": args.data_path,
                "checkpoint_path": args.checkpoint_path,
                "device": str(device),
                "num_samples": num_samples,
                "steps": int(args.steps),
                "seed": int(args.seed),
                "ablate": sweep_param,
                "values": sweep_values,
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
            "rows": rows,
            "scenario_summary": scenario_summary,
            "random_ood_summary": random_summary,
        }

        json_out = _expand_output_path(json_path, json_path.suffix, sweep_param)
        markdown_out = _expand_output_path(markdown_path, markdown_path.suffix, sweep_param)
        csv_out = _expand_output_path(csv_path, csv_path.suffix, sweep_param)
        json_out.parent.mkdir(parents=True, exist_ok=True)
        markdown_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(results, indent=2), encoding="utf-8")
        markdown_out.write_text(format_markdown(results), encoding="utf-8")
        write_csv(rows, csv_out)

        print(format_markdown(results))
        print(f"Saved JSON results: {json_out}")
        print(f"Saved Markdown summary: {markdown_out}")
        print(f"Saved CSV (Pareto): {csv_out}")
        if args.plot:
            plot_paths = plot_ablation(
                rows=rows,
                sweep_param=sweep_param,
                output_dir=Path(args.plot_dir),
            )
            if plot_paths:
                print("Saved ablation plots:")
                for path in plot_paths:
                    print(f"- {path}")


if __name__ == "__main__":
    main()
