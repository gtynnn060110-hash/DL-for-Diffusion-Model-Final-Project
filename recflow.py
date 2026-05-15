import argparse
from pathlib import Path

import numpy as np
import torch

from model import build_model, get_default_device


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Phase4: Rectified Flow inference and 3D visualization."
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


@torch.no_grad()
def euler_sample(model: torch.nn.Module, num_samples: int, seq_len: int, point_dim: int, steps: int, device: torch.device) -> torch.Tensor:
    if steps <= 0:
        raise ValueError("steps must be positive.")
    if num_samples <= 0:
        raise ValueError("num_samples must be positive.")

    z = torch.randn(num_samples, seq_len, point_dim, device=device, dtype=torch.float32)
    dt = 1.0 / float(steps)

    for i in range(steps):
        t_scalar = i / float(steps)
        t = torch.full((num_samples, 1), t_scalar, device=device, dtype=torch.float32)
        v = model(z, t)
        z = z + v * dt
        if not torch.isfinite(z).all():
            raise RuntimeError(f"Non-finite values encountered during Euler step {i}.")
    return z


def visualize_comparison(real: np.ndarray, generated: np.ndarray, save_fig: Path | None, no_show: bool) -> None:
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(14, 6))
    ax_real = fig.add_subplot(121, projection="3d")
    ax_gen = fig.add_subplot(122, projection="3d")

    for traj in real:
        ax_real.plot(traj[:, 0], traj[:, 1], traj[:, 2], color="tab:blue", alpha=0.75, linewidth=1.2)
    ax_real.scatter([-5.0], [0.0], [0.0], color="green", s=50, label="start")
    ax_real.scatter([5.0], [0.0], [0.0], color="red", s=50, label="end")
    ax_real.scatter([0.0], [0.0], [0.0], color="black", s=40, label="obstacle")
    ax_real.set_title("Real trajectories (X1)")
    ax_real.set_xlabel("x")
    ax_real.set_ylabel("y")
    ax_real.set_zlabel("z")
    ax_real.legend(loc="upper left")

    for traj in generated:
        ax_gen.plot(traj[:, 0], traj[:, 1], traj[:, 2], color="tab:orange", alpha=0.75, linewidth=1.2)
    ax_gen.scatter([-5.0], [0.0], [0.0], color="green", s=50, label="start")
    ax_gen.scatter([5.0], [0.0], [0.0], color="red", s=50, label="end")
    ax_gen.scatter([0.0], [0.0], [0.0], color="black", s=40, label="obstacle")
    ax_gen.set_title("Generated trajectories (Z1)")
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

    model = load_model_from_checkpoint(
        checkpoint_path=Path(args.checkpoint_path),
        seq_len=seq_len,
        point_dim=point_dim,
        device=device,
    )
    generated = euler_sample(
        model=model,
        num_samples=count,
        seq_len=seq_len,
        point_dim=point_dim,
        steps=int(args.steps),
        device=device,
    ).detach().cpu().numpy().astype(np.float32)

    if args.save_generated:
        output = Path(args.save_generated)
        output.parent.mkdir(parents=True, exist_ok=True)
        np.save(output, generated)
        print(f"Saved generated trajectories: {generated.shape} -> {output}")

    print(f"Device: {device}")
    print(f"Real subset shape: {real_subset.shape}, Generated shape: {generated.shape}")
    save_fig = Path(args.save_fig) if args.save_fig else None
    visualize_comparison(real_subset, generated, save_fig=save_fig, no_show=args.no_show)


if __name__ == "__main__":
    main()
