import _bootstrap  # noqa: E402, F401 — must precede rectified_flow imports

import argparse
from pathlib import Path

import numpy as np
import torch

from rectified_flow.sampling import (
    guided_euler_sample,
    load_model_from_checkpoint,
    load_real_data,
    obstacle_distance_stats,
    set_seed,
)
from rectified_flow.model import get_default_device


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Energy-guided Rectified Flow inference and 3D visualization."
    )
    parser.add_argument("--checkpoint-path", type=str, default="checkpoints/rectified_flow_mlp.pt")
    parser.add_argument("--data-path", type=str, default="dataset/toy_trajectories.npy")
    parser.add_argument("--num-samples", type=int, default=20, help="Number of trajectories to generate/show.")
    parser.add_argument("--steps", type=int, default=10, help="Euler integration steps.")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--device",
        type=str,
        default="auto",
        choices=["auto", "cpu", "cuda", "mps"],
        help="Inference device. auto = cuda -> mps -> cpu",
    )
    parser.add_argument("--save-fig", type=str, default="", help="Optional path to save comparison figure.")
    parser.add_argument("--save-generated", type=str, default="", help="Optional path to save generated trajectories (.npy).")
    parser.add_argument("--no-show", action="store_true", help="Disable interactive figure window.")
    parser.add_argument(
        "--obstacle-center",
        type=float,
        nargs=3,
        default=(0.0, 0.0, 0.0),
        metavar=("X", "Y", "Z"),
        help="Center of the spherical obstacle.",
    )
    parser.add_argument("--obstacle-radius", type=float, default=1.0, help="Radius of the spherical obstacle.")
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
    parser.add_argument("--guidance-scale", type=float, default=1.0, help="Strength of the obstacle repulsion.")
    parser.add_argument(
        "--guidance-margin",
        type=float,
        default=1.0,
        help="Extra distance outside the obstacle where guidance becomes active.",
    )
    parser.add_argument(
        "--guidance-decay",
        type=str,
        default="distance_gated",
        choices=["constant", "distance_gated"],
        help="Schedule or adaptive mode for the guidance strength.",
    )
    parser.add_argument(
        "--max-guidance-norm",
        type=float,
        default=5.0,
        help="Per-point guidance norm clipping value; 0 disables clipping.",
    )
    return parser.parse_args()


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


def visualize_comparison(
    real: np.ndarray,
    generated: np.ndarray,
    obstacle_centers: np.ndarray,
    save_fig: Path | None,
    no_show: bool,
) -> None:
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(14, 6))
    ax_real = fig.add_subplot(121, projection="3d")
    ax_gen = fig.add_subplot(122, projection="3d")

    for traj in real:
        ax_real.plot(traj[:, 0], traj[:, 1], traj[:, 2], color="tab:blue", alpha=0.75, linewidth=1.2)
    ax_real.scatter([-5.0], [0.0], [0.0], color="green", s=50, label="start")
    ax_real.scatter([5.0], [0.0], [0.0], color="red", s=50, label="end")
    ax_real.scatter(
        obstacle_centers[:, 0], obstacle_centers[:, 1], obstacle_centers[:, 2],
        color="black", s=40, label="obstacle"
    )
    ax_real.set_title("Real trajectories (X1)")
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
        color="black", s=40, label="obstacle"
    )
    ax_gen.set_title("Energy-guided generated trajectories (Z1)")
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

    real_all = load_real_data(Path(args.data_path))
    seq_len = int(real_all.shape[1])
    point_dim = int(real_all.shape[2])
    count = min(int(args.num_samples), int(real_all.shape[0]))
    real_subset = real_all[:count]

    obstacle_centers_np, obstacle_radii_np = resolve_obstacles(args)
    obstacle_centers = torch.tensor(obstacle_centers_np, device=device, dtype=torch.float32)
    obstacle_radii = torch.tensor(obstacle_radii_np, device=device, dtype=torch.float32)

    model = load_model_from_checkpoint(
        checkpoint_path=Path(args.checkpoint_path),
        seq_len=seq_len,
        point_dim=point_dim,
        device=device,
    )
    generated = guided_euler_sample(
        model=model,
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
    ).detach().cpu().numpy().astype(np.float32)

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
    print(f"Real subset shape: {real_subset.shape}, Generated shape: {generated.shape}")
    print(
        "Guidance: "
        f"obstacles={[(tuple(float(v) for v in center), float(radius)) for center, radius in zip(obstacle_centers_np, obstacle_radii_np)]}, "
        f"scale={float(args.guidance_scale):.4f}, "
        f"margin={float(args.guidance_margin):.4f}, "
        f"decay={args.guidance_decay}, "
        f"max_norm={float(args.max_guidance_norm):.4f}"
    )
    print(
        "Real obstacle stats: "
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
        save_fig=save_fig,
        no_show=args.no_show,
    )


if __name__ == "__main__":
    main()
