import argparse
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from model import build_conditional_model
from train import resolve_device, set_seed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train conditional 1-Rectified Flow on obstacle-conditioned trajectory data."
    )
    parser.add_argument("--data-path", type=str, default="dataset/conditional_trajectories.npz")
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
        "--checkpoint-path",
        type=str,
        default="checkpoints/rectified_flow_conditional_mlp.pt",
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


def load_conditional_tensors(data_path: Path) -> tuple[torch.Tensor, torch.Tensor]:
    if not data_path.exists():
        raise FileNotFoundError(f"Conditional dataset file not found: {data_path}")
    data = np.load(data_path)
    if "trajectories" not in data or "conditions" not in data:
        raise ValueError("Conditional dataset must contain `trajectories` and `conditions` arrays.")

    trajectories = data["trajectories"]
    conditions = data["conditions"]
    if trajectories.ndim != 3 or trajectories.shape[-1] != 3:
        raise ValueError(f"Expected trajectories shape (N, T, 3), got {trajectories.shape}.")
    if conditions.ndim != 2 or conditions.shape[0] != trajectories.shape[0]:
        raise ValueError(
            "Expected conditions shape (N, C) with the same N as trajectories, "
            f"got {conditions.shape} and {trajectories.shape}."
        )
    if not np.isfinite(trajectories).all() or not np.isfinite(conditions).all():
        raise ValueError("Conditional dataset contains NaN or Inf values.")

    return (
        torch.from_numpy(trajectories.astype(np.float32, copy=False)),
        torch.from_numpy(conditions.astype(np.float32, copy=False)),
    )


def save_checkpoint(
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    epoch: int,
    loss: float,
    checkpoint_path: Path,
    args: argparse.Namespace,
    condition_dim: int,
) -> None:
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    checkpoint_args = dict(vars(args))
    checkpoint_args["condition_dim"] = int(condition_dim)
    torch.save(
        {
            "epoch": epoch,
            "loss": loss,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "args": checkpoint_args,
        },
        checkpoint_path,
    )


def train() -> None:
    args = parse_args()
    set_seed(args.seed)

    device = resolve_device(args.device)
    data_path = Path(args.data_path)
    x1_all, conditions_all = load_conditional_tensors(data_path)

    dataset = TensorDataset(x1_all, conditions_all)
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
    condition_dim = conditions_all.shape[1]
    model = build_conditional_model(
        seq_len=seq_len,
        point_dim=point_dim,
        condition_dim=condition_dim,
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
    print(f"Dataset: trajectories={tuple(x1_all.shape)}, conditions={tuple(conditions_all.shape)} from {data_path}")
    print(
        "Trajectory stats: "
        f"dtype={x1_all.dtype}, min={x1_all.min().item():.4f}, "
        f"max={x1_all.max().item():.4f}, std={x1_all.std().item():.4f}"
    )
    print(
        "Condition stats: "
        f"dtype={conditions_all.dtype}, min={conditions_all.min().item():.4f}, "
        f"max={conditions_all.max().item():.4f}, std={conditions_all.std().item():.4f}"
    )

    epoch_loss = float("nan")
    for epoch in range(1, args.epochs + 1):
        model.train()
        total_loss = 0.0
        total_samples = 0

        for x1_batch, condition_batch in dataloader:
            x1_batch = x1_batch.to(
                device=device, dtype=torch.float32, non_blocking=(device.type == "cuda")
            ).contiguous()
            condition_batch = condition_batch.to(
                device=device, dtype=torch.float32, non_blocking=(device.type == "cuda")
            ).contiguous()
            batch_size = x1_batch.shape[0]

            x0_batch = torch.randn_like(x1_batch)
            t = torch.rand(batch_size, 1, 1, device=device, dtype=torch.float32)
            xt_batch = t * x1_batch + (1.0 - t) * x0_batch
            v_target = x1_batch - x0_batch

            v_pred = model(xt_batch, t.view(batch_size, 1), condition_batch)
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
            save_checkpoint(model, optimizer, epoch, epoch_loss, ckpt_path, args, condition_dim)
            print(f"Saved checkpoint: {ckpt_path}")

    final_checkpoint_path = Path(args.checkpoint_path)
    save_checkpoint(
        model, optimizer, args.epochs, epoch_loss, final_checkpoint_path, args, condition_dim
    )
    print(f"Training finished. Final checkpoint: {final_checkpoint_path}")


if __name__ == "__main__":
    train()
