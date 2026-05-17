import argparse
from pathlib import Path

import numpy as np
import torch

from model import build_model, get_default_device


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
        default="linear",
        choices=["constant", "linear"],
        help="Time schedule for the guidance strength.",
    )
    parser.add_argument(
        "--max-guidance-norm",
        type=float,
        default=5.0,
        help="Per-point guidance norm clipping value; 0 disables clipping.",
    )
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


def set_seed(seed: int) -> None:
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def load_real_data(data_path: Path) -> np.ndarray:
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    real = np.load(data_path)
    if real.ndim != 3 or real.shape[-1] != 3:
        raise ValueError(f"Expected data shape (N, T, 3), got {real.shape}.")
    if not np.isfinite(real).all():
        raise ValueError("Dataset contains NaN or Inf values.")
    return real.astype(np.float32, copy=False)


def load_model_from_checkpoint(
    checkpoint_path: Path,
    seq_len: int,
    point_dim: int,
    device: torch.device,
) -> torch.nn.Module:
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")

    checkpoint = torch.load(checkpoint_path, map_location="cpu")
    if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
        state_dict = checkpoint["model_state_dict"]
        ckpt_args = checkpoint.get("args", {})
    elif isinstance(checkpoint, dict):
        state_dict = checkpoint
        ckpt_args = {}
    else:
        raise ValueError("Unsupported checkpoint format.")

    model = build_model(
        seq_len=seq_len,
        point_dim=point_dim,
        hidden_dim=int(ckpt_args.get("hidden_dim", 512)),
        time_embedding_dim=int(ckpt_args.get("time_embedding_dim", 64)),
        num_hidden_layers=int(ckpt_args.get("num_hidden_layers", 3)),
        device=device,
    )
    model.load_state_dict(state_dict, strict=True)
    model.eval()
    return model


def compute_obstacle_energy_gradient(
    z: torch.Tensor,
    obstacle_center: torch.Tensor,
    obstacle_radius: float,
    guidance_margin: float,
    eps: float = 1e-6,
) -> torch.Tensor:
    if obstacle_radius < 0.0:
        raise ValueError("obstacle_radius must be non-negative.")
    if guidance_margin < 0.0:
        raise ValueError("guidance_margin must be non-negative.")

    center = obstacle_center.view(1, 1, 3).to(device=z.device, dtype=z.dtype)
    offset = z - center
    distance = torch.linalg.norm(offset, dim=-1, keepdim=True).clamp_min(eps)
    direction = offset / distance
    active_distance = float(obstacle_radius + guidance_margin)
    penalty = torch.clamp(active_distance - distance, min=0.0)
    return -penalty * direction


def guidance_strength(t_scalar: float, guidance_scale: float, guidance_decay: str) -> float:
    if guidance_decay == "constant":
        return guidance_scale
    if guidance_decay == "linear":
        return guidance_scale * (1.0 - t_scalar)
    raise ValueError(f"Unsupported guidance_decay: {guidance_decay}")


@torch.no_grad()
def guided_euler_sample(
    model: torch.nn.Module,
    num_samples: int,
    seq_len: int,
    point_dim: int,
    steps: int,
    device: torch.device,
    obstacle_center: torch.Tensor,
    obstacle_radius: float,
    guidance_scale: float,
    guidance_margin: float,
    guidance_decay: str,
    max_guidance_norm: float,
) -> torch.Tensor:
    if steps <= 0:
        raise ValueError("steps must be positive.")
    if num_samples <= 0:
        raise ValueError("num_samples must be positive.")
    if point_dim != 3:
        raise ValueError("Energy guidance expects 3D trajectory points.")

    z = torch.randn(num_samples, seq_len, point_dim, device=device, dtype=torch.float32)
    dt = 1.0 / float(steps)

    for i in range(steps):
        t_scalar = i / float(steps)
        t = torch.full((num_samples, 1), t_scalar, device=device, dtype=torch.float32)
        v = model(z, t)
        grad_e = compute_obstacle_energy_gradient(
            z=z,
            obstacle_center=obstacle_center,
            obstacle_radius=obstacle_radius,
            guidance_margin=guidance_margin,
        )
        lambda_t = guidance_strength(t_scalar, guidance_scale, guidance_decay)
        guidance = lambda_t * grad_e

        if max_guidance_norm > 0.0:
            norm = torch.linalg.norm(guidance, dim=-1, keepdim=True).clamp_min(1e-6)
            guidance = guidance * torch.clamp(max_guidance_norm / norm, max=1.0)

        z = z + (v - guidance) * dt
        if not torch.isfinite(z).all():
            raise RuntimeError(f"Non-finite values encountered during guided Euler step {i}.")
    return z


def obstacle_distance_stats(
    trajectories: np.ndarray,
    obstacle_center: np.ndarray,
    obstacle_radius: float,
) -> tuple[float, float, float]:
    if trajectories.ndim != 3 or trajectories.shape[-1] != 3:
        raise ValueError(f"Expected trajectories shape (N, T, 3), got {trajectories.shape}.")

    distances = np.linalg.norm(trajectories - obstacle_center.reshape(1, 1, 3), axis=-1)
    min_per_trajectory = distances.min(axis=1)
    collision_rate = float(np.mean(min_per_trajectory <= obstacle_radius))
    success_rate = 1.0 - collision_rate
    min_distance = float(min_per_trajectory.min())
    return collision_rate, success_rate, min_distance


def visualize_comparison(
    real: np.ndarray,
    generated: np.ndarray,
    obstacle_center: np.ndarray,
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
        [obstacle_center[0]], [obstacle_center[1]], [obstacle_center[2]],
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
        [obstacle_center[0]], [obstacle_center[1]], [obstacle_center[2]],
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

    obstacle_center_np = np.asarray(args.obstacle_center, dtype=np.float32)
    obstacle_center = torch.tensor(obstacle_center_np, device=device, dtype=torch.float32)

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
        obstacle_center=obstacle_center,
        obstacle_radius=float(args.obstacle_radius),
        guidance_scale=float(args.guidance_scale),
        guidance_margin=float(args.guidance_margin),
        guidance_decay=str(args.guidance_decay),
        max_guidance_norm=float(args.max_guidance_norm),
    ).detach().cpu().numpy().astype(np.float32)

    if args.save_generated:
        output = Path(args.save_generated)
        output.parent.mkdir(parents=True, exist_ok=True)
        np.save(output, generated)
        print(f"Saved generated trajectories: {generated.shape} -> {output}")

    real_collision, real_success, real_min_distance = obstacle_distance_stats(
        real_subset,
        obstacle_center_np,
        float(args.obstacle_radius),
    )
    generated_collision, generated_success, generated_min_distance = obstacle_distance_stats(
        generated,
        obstacle_center_np,
        float(args.obstacle_radius),
    )

    print(f"Device: {device}")
    print(f"Real subset shape: {real_subset.shape}, Generated shape: {generated.shape}")
    print(
        "Guidance: "
        f"center={tuple(float(x) for x in obstacle_center_np)}, "
        f"radius={float(args.obstacle_radius):.4f}, "
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
        obstacle_center=obstacle_center_np,
        save_fig=save_fig,
        no_show=args.no_show,
    )


if __name__ == "__main__":
    main()
