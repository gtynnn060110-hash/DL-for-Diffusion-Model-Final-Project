import _bootstrap  # noqa: E402, F401 — must precede rectified_flow imports

import argparse
from pathlib import Path

import numpy as np
import torch

from rectified_flow.sampling import (
    conditional_euler_sample,
    conditional_guided_euler_sample,
    load_conditional_model_from_checkpoint,
    make_obstacle_condition,
    obstacle_distance_stats,
    set_seed,
)
from rectified_flow.model import get_default_device


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Conditional Rectified Flow inference and 3D visualization."
    )
    parser.add_argument(
        "--checkpoint-path",
        type=str,
        default="checkpoints/rectified_flow_conditional_mlp.pt",
    )
    parser.add_argument(
        "--data-path",
        type=str,
        default="dataset/conditional_trajectories.npz",
        help="Reference trajectories: .npz with `trajectories` or .npy with shape (N,T,3).",
    )
    parser.add_argument("--num-samples", type=int, default=20)
    parser.add_argument("--steps", type=int, default=20)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--device",
        type=str,
        default="auto",
        choices=["auto", "cpu", "cuda", "mps"],
        help="Inference device. auto = cuda -> mps -> cpu",
    )
    parser.add_argument("--save-fig", type=str, default="")
    parser.add_argument("--save-generated", type=str, default="")
    parser.add_argument("--no-show", action="store_true")
    parser.add_argument(
        "--obstacle-center",
        type=float,
        nargs=3,
        default=(0.0, 1.5, 0.0),
        metavar=("X", "Y", "Z"),
        help="Center of the spherical obstacle.",
    )
    parser.add_argument("--obstacle-radius", type=float, default=1.0)
    parser.add_argument(
        "--obstacle",
        action="append",
        nargs=4,
        type=float,
        metavar=("X", "Y", "Z", "R"),
        help=(
            "Spherical obstacle as X Y Z R. Can be repeated. "
            "When provided, overrides --obstacle-center/--obstacle-radius."
        ),
    )
    parser.add_argument(
        "--guided",
        action="store_true",
        help="Apply energy guidance on top of the conditional model.",
    )
    parser.add_argument("--guidance-scale", type=float, default=3.0)
    parser.add_argument("--guidance-margin", type=float, default=2.0)
    parser.add_argument(
        "--guidance-decay",
        type=str,
        default="distance_gated",
        choices=["constant", "distance_gated"],
    )
    parser.add_argument("--max-guidance-norm", type=float, default=10.0)
    return parser.parse_args()


def resolve_device(device_arg: str) -> torch.device:
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


def load_reference_trajectories(data_path: Path) -> np.ndarray:
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")

    if data_path.suffix == ".npz":
        data = np.load(data_path)
        if "trajectories" not in data:
            raise ValueError("Expected .npz data to contain a `trajectories` array.")
        trajectories = data["trajectories"]
    else:
        trajectories = np.load(data_path)

    if trajectories.ndim != 3 or trajectories.shape[-1] != 3:
        raise ValueError(f"Expected trajectories shape (N, T, 3), got {trajectories.shape}.")
    if not np.isfinite(trajectories).all():
        raise ValueError("Reference trajectories contain NaN or Inf values.")
    return trajectories.astype(np.float32, copy=False)


def resolve_obstacles(args: argparse.Namespace) -> tuple[np.ndarray, np.ndarray]:
    if args.obstacle:
        obstacle_array = np.asarray(args.obstacle, dtype=np.float32)
        centers = obstacle_array[:, :3]
        radii = obstacle_array[:, 3]
    else:
        centers = np.asarray(args.obstacle_center, dtype=np.float32).reshape(1, 3)
        radii = np.asarray([args.obstacle_radius], dtype=np.float32)
    if np.any(radii < 0.0):
        raise ValueError("Obstacle radii must be non-negative.")
    return centers, radii


def visualize_comparison(
    real: np.ndarray,
    generated: np.ndarray,
    obstacle_centers: np.ndarray,
    title: str,
    save_fig: Path | None,
    no_show: bool,
) -> None:
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(14, 6))
    ax_real = fig.add_subplot(121, projection="3d")
    ax_gen = fig.add_subplot(122, projection="3d")

    for traj in real:
        ax_real.plot(traj[:, 0], traj[:, 1], traj[:, 2], color="tab:blue", alpha=0.65, linewidth=1.2)
    ax_real.scatter([-5.0], [0.0], [0.0], color="green", s=50, label="start")
    ax_real.scatter([5.0], [0.0], [0.0], color="red", s=50, label="end")
    ax_real.scatter(
        obstacle_centers[:, 0], obstacle_centers[:, 1], obstacle_centers[:, 2],
        color="black", s=45, label="obstacle"
    )
    ax_real.set_title("Reference trajectories")
    ax_real.set_xlabel("x")
    ax_real.set_ylabel("y")
    ax_real.set_zlabel("z")
    ax_real.legend(loc="upper left")

    for traj in generated:
        ax_gen.plot(traj[:, 0], traj[:, 1], traj[:, 2], color="tab:orange", alpha=0.75, linewidth=1.2)
    ax_gen.scatter([-5.0], [0.0], [0.0], color="green", s=50, label="start")
    ax_gen.scatter([5.0], [0.0], [0.0], color="red", s=50, label="end")
    ax_gen.scatter(
        obstacle_centers[:, 0], obstacle_centers[:, 1], obstacle_centers[:, 2],
        color="black", s=45, label="obstacle"
    )
    ax_gen.set_title(title)
    ax_gen.set_xlabel("x")
    ax_gen.set_ylabel("y")
    ax_gen.set_zlabel("z")
    ax_gen.legend(loc="upper left")

    if save_fig is not None:
        save_fig.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_fig, dpi=150, bbox_inches="tight")
        print(f"Saved figure: {save_fig}")
    if not no_show:
        plt.show()


def main() -> None:
    args = parse_args()
    set_seed(args.seed)
    device = resolve_device(args.device)

    real_all = load_reference_trajectories(Path(args.data_path))
    seq_len = int(real_all.shape[1])
    point_dim = int(real_all.shape[2])
    count = min(int(args.num_samples), int(real_all.shape[0]))
    real_subset = real_all[:count]
    obstacle_centers_np, obstacle_radii_np = resolve_obstacles(args)

    model = load_conditional_model_from_checkpoint(
        checkpoint_path=Path(args.checkpoint_path),
        seq_len=seq_len,
        point_dim=point_dim,
        device=device,
    )
    condition = make_obstacle_condition(
        obstacle_centers=torch.tensor(obstacle_centers_np, device=device, dtype=torch.float32),
        obstacle_radii=torch.tensor(obstacle_radii_np, device=device, dtype=torch.float32),
        condition_dim=int(getattr(model, "condition_dim")),
    )
    obstacle_centers = torch.tensor(obstacle_centers_np, device=device, dtype=torch.float32)
    obstacle_radii = torch.tensor(obstacle_radii_np, device=device, dtype=torch.float32)

    if args.guided:
        generated_tensor = conditional_guided_euler_sample(
            model=model,
            condition=condition,
            num_samples=count,
            seq_len=seq_len,
            point_dim=point_dim,
            steps=int(args.steps),
            device=device,
            obstacle_center=obstacle_centers[0],
            obstacle_radius=float(obstacle_radii[0].item()),
            guidance_scale=float(args.guidance_scale),
            guidance_margin=float(args.guidance_margin),
            guidance_decay=str(args.guidance_decay),
            max_guidance_norm=float(args.max_guidance_norm),
            obstacle_centers=obstacle_centers,
            obstacle_radii=obstacle_radii,
        )
        title = f"Conditional + guided ({args.guidance_decay})"
    else:
        generated_tensor = conditional_euler_sample(
            model=model,
            condition=condition,
            num_samples=count,
            seq_len=seq_len,
            point_dim=point_dim,
            steps=int(args.steps),
            device=device,
        )
        title = "Conditional generated trajectories"

    generated = generated_tensor.detach().cpu().numpy().astype(np.float32)

    if args.save_generated:
        output = Path(args.save_generated)
        output.parent.mkdir(parents=True, exist_ok=True)
        np.save(output, generated)
        print(f"Saved generated trajectories: {generated.shape} -> {output}")

    real_collision, real_success, real_min_distance = obstacle_distance_stats(
        real_subset,
        obstacle_centers_np,
        obstacle_radii_np,
    )
    generated_collision, generated_success, generated_min_distance = obstacle_distance_stats(
        generated,
        obstacle_centers_np,
        obstacle_radii_np,
    )

    print(f"Device: {device}")
    print(f"Reference shape: {real_subset.shape}, Generated shape: {generated.shape}")
    print(
        "Condition obstacles: "
        f"{[(tuple(float(v) for v in center), float(radius)) for center, radius in zip(obstacle_centers_np, obstacle_radii_np)]}"
    )
    print(
        "Reference obstacle stats: "
        f"collision_rate={real_collision:.4f}, "
        f"success_rate={real_success:.4f}, "
        f"min_distance={real_min_distance:.4f}"
    )
    print(
        "Generated obstacle stats: "
        f"collision_rate={generated_collision:.4f}, "
        f"success_rate={generated_success:.4f}, "
        f"min_distance={generated_min_distance:.4f}"
    )

    save_fig = Path(args.save_fig) if args.save_fig else None
    visualize_comparison(
        real_subset,
        generated,
        obstacle_centers=obstacle_centers_np,
        title=title,
        save_fig=save_fig,
        no_show=args.no_show,
    )


if __name__ == "__main__":
    main()
