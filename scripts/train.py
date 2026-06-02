import _bootstrap  # noqa: E402, F401 — must precede rectified_flow imports

import argparse
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from rectified_flow.model import build_model, get_default_device


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train 1-Rectified Flow on 3D trajectory data."
    )
    parser.add_argument("--data-path", type=str, default="dataset/toy_trajectories.npy")
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--epochs", type=int, default=200)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--weight-decay", type=float, default=0.0)
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--hidden-dim", type=int, default=512)
    parser.add_argument("--time-embedding-dim", type=int, default=64)
    parser.add_argument("--num-hidden-layers", type=int, default=3)
    parser.add_argument(
        "--checkpoint-path", type=str, default="checkpoints/rectified_flow_mlp.pt"
    )
    parser.add_argument(
        "--save-every",
        type=int,
        default=0,
        help="Save checkpoint every N epochs; 0 disables.",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="auto",
        choices=["auto", "cpu", "cuda", "mps"],
        help="Training device. auto = cuda -> mps -> cpu",
    )
    parser.add_argument(
        "--grad-clip-norm",
        type=float,
        default=1.0,
        help="0 disables gradient clipping.",
    )
    return parser.parse_args()


def set_seed(seed: int) -> None:
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def load_trajectory_tensor(data_path: Path) -> torch.Tensor:
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset file not found: {data_path}")
    data = np.load(data_path)
    if data.ndim != 3 or data.shape[-1] != 3:
        raise ValueError(f"Expected data shape (N, T, 3), got {data.shape}.")
    if not np.isfinite(data).all():
        raise ValueError("Dataset contains NaN or Inf values.")
    data = data.astype(np.float32, copy=False)
    return torch.from_numpy(data)


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


def save_checkpoint(
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    epoch: int,
    loss: float,
    checkpoint_path: Path,
    args: argparse.Namespace,
) -> None:
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "epoch": epoch,
            "loss": loss,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "args": vars(args),
        },
        checkpoint_path,
    )


def train() -> None:
    args = parse_args()
    set_seed(args.seed)

    device = resolve_device(args.device)
    data_path = Path(args.data_path)
    x1_all = load_trajectory_tensor(data_path)

    dataset = TensorDataset(x1_all)
    dataloader = DataLoader(
        dataset,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=args.num_workers,
        pin_memory=(device.type == "cuda"),
        drop_last=False,
    )

    seq_len = x1_all.shape[1]
    point_dim = x1_all.shape[2]
    model = build_model(
        seq_len=seq_len,
        point_dim=point_dim,
        hidden_dim=args.hidden_dim,
        time_embedding_dim=args.time_embedding_dim,
        num_hidden_layers=args.num_hidden_layers,
        device=device,
    )
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=args.lr,
        weight_decay=args.weight_decay,
    )

    print(f"Device: {device}")
    print(f"Dataset: {tuple(x1_all.shape)} from {data_path}")
    print(
        "Data stats: "
        f"dtype={x1_all.dtype}, min={x1_all.min().item():.4f}, "
        f"max={x1_all.max().item():.4f}, std={x1_all.std().item():.4f}"
    )

    for epoch in range(1, args.epochs + 1):
        model.train()
        total_loss = 0.0
        total_samples = 0

        for (x1_batch,) in dataloader:
            x1_batch = x1_batch.to(
                device=device, dtype=torch.float32, non_blocking=(device == "cuda")
            ).contiguous()
            batch_size = x1_batch.shape[0]

            x0_batch = torch.randn_like(x1_batch)
            t = torch.rand(batch_size, 1, 1, device=device, dtype=torch.float32)
            xt_batch = t * x1_batch + (1.0 - t) * x0_batch
            v_target = x1_batch - x0_batch

            v_pred = model(xt_batch, t.view(batch_size, 1))
            loss = F.mse_loss(v_pred, v_target)

            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            if args.grad_clip_norm > 0:
                torch.nn.utils.clip_grad_norm_(model.parameters(), args.grad_clip_norm)
            optimizer.step()

            total_loss += loss.item() * batch_size
            total_samples += batch_size

        epoch_loss = total_loss / max(total_samples, 1)
        print(f"Epoch [{epoch}/{args.epochs}] loss={epoch_loss:.6f}")

        if args.save_every > 0 and epoch % args.save_every == 0:
            ckpt_path = Path(args.checkpoint_path)
            save_checkpoint(model, optimizer, epoch, epoch_loss, ckpt_path, args)
            print(f"Saved checkpoint: {ckpt_path}")

    final_checkpoint_path = Path(args.checkpoint_path)
    save_checkpoint(
        model, optimizer, args.epochs, epoch_loss, final_checkpoint_path, args
    )
    print(f"Training finished. Final checkpoint: {final_checkpoint_path}")


if __name__ == "__main__":
    train()
