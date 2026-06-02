"""Shared Rectified Flow sampling and spherical obstacle energy guidance."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import torch

from rectified_flow.model import build_conditional_model, build_model


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


def load_conditional_model_from_checkpoint(
    checkpoint_path: Path,
    seq_len: int,
    point_dim: int,
    device: torch.device,
) -> torch.nn.Module:
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Conditional checkpoint not found: {checkpoint_path}")

    checkpoint = torch.load(checkpoint_path, map_location="cpu")
    if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
        state_dict = checkpoint["model_state_dict"]
        ckpt_args = checkpoint.get("args", {})
    elif isinstance(checkpoint, dict):
        state_dict = checkpoint
        ckpt_args = {}
    else:
        raise ValueError("Unsupported conditional checkpoint format.")

    condition_dim = int(ckpt_args.get("condition_dim", ckpt_args.get("max_obstacles", 1) * 4))
    model = build_conditional_model(
        seq_len=seq_len,
        point_dim=point_dim,
        condition_dim=condition_dim,
        hidden_dim=int(ckpt_args.get("hidden_dim", 512)),
        time_embedding_dim=int(ckpt_args.get("time_embedding_dim", 64)),
        num_hidden_layers=int(ckpt_args.get("num_hidden_layers", 3)),
        device=device,
    )
    model.load_state_dict(state_dict, strict=True)
    model.eval()
    return model


def make_initial_noise(
    num_samples: int,
    seq_len: int,
    point_dim: int,
    device: torch.device,
    z_init: torch.Tensor | None = None,
) -> torch.Tensor:
    """Return initial latent state z_0, optionally from a caller-provided tensor."""
    expected_shape = (num_samples, seq_len, point_dim)
    if z_init is None:
        return torch.randn(expected_shape, device=device, dtype=torch.float32)
    if tuple(z_init.shape) != expected_shape:
        raise ValueError(
            f"z_init must have shape {expected_shape}, got {tuple(z_init.shape)}."
        )
    return z_init.to(device=device, dtype=torch.float32).clone()


def make_obstacle_condition(
    obstacle_centers: torch.Tensor,
    obstacle_radii: torch.Tensor,
    condition_dim: int,
) -> torch.Tensor:
    if condition_dim <= 0 or condition_dim % 4 != 0:
        raise ValueError("condition_dim must be a positive multiple of 4.")

    centers = obstacle_centers.to(dtype=torch.float32)
    radii = obstacle_radii.to(dtype=torch.float32).flatten()
    if centers.ndim == 1:
        centers = centers.view(1, 3)
    if centers.ndim != 2 or centers.shape[-1] != 3:
        raise ValueError(f"obstacle_centers must have shape (M, 3), got {tuple(centers.shape)}.")
    if radii.ndim != 1 or radii.shape[0] != centers.shape[0]:
        raise ValueError("obstacle_radii must have shape (M,) and match obstacle_centers.")

    max_obstacles = condition_dim // 4
    if centers.shape[0] > max_obstacles:
        raise ValueError(
            f"Conditional model supports at most {max_obstacles} obstacles, got {centers.shape[0]}."
        )

    condition = torch.zeros((condition_dim,), device=centers.device, dtype=torch.float32)
    for idx, (center, radius) in enumerate(zip(centers, radii)):
        start = idx * 4
        condition[start : start + 3] = center
        condition[start + 3] = radius
    return condition


def prepare_condition_batch(
    condition: torch.Tensor,
    num_samples: int,
    device: torch.device,
) -> torch.Tensor:
    if condition.ndim == 1:
        condition = condition.view(1, -1)
    if condition.ndim != 2:
        raise ValueError(f"condition must have shape (C,) or (N, C), got {tuple(condition.shape)}.")
    if condition.shape[0] == 1 and num_samples > 1:
        condition = condition.repeat(num_samples, 1)
    if condition.shape[0] != num_samples:
        raise ValueError(
            f"condition batch size must be 1 or {num_samples}, got {condition.shape[0]}."
        )
    return condition.to(device=device, dtype=torch.float32).clone()


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


def compute_multi_obstacle_energy_gradient(
    z: torch.Tensor,
    obstacle_centers: torch.Tensor,
    obstacle_radii: torch.Tensor,
    guidance_margin: float,
) -> torch.Tensor:
    centers = obstacle_centers.to(device=z.device, dtype=z.dtype)
    radii = obstacle_radii.to(device=z.device, dtype=z.dtype).flatten()
    if centers.ndim != 2 or centers.shape[-1] != 3:
        raise ValueError(f"obstacle_centers must have shape (M, 3), got {tuple(centers.shape)}.")
    if radii.ndim != 1 or radii.shape[0] != centers.shape[0]:
        raise ValueError("obstacle_radii must have shape (M,) and match obstacle_centers.")
    if centers.shape[0] <= 0:
        raise ValueError("At least one obstacle is required.")

    total = torch.zeros_like(z)
    for center, radius in zip(centers, radii):
        total = total + compute_obstacle_energy_gradient(
            z=z,
            obstacle_center=center,
            obstacle_radius=float(radius.item()),
            guidance_margin=guidance_margin,
        )
    return total


def compute_obstacle_distance_gate(
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
    distance = torch.linalg.norm(z - center, dim=-1, keepdim=True).clamp_min(eps)
    signed_clearance = distance - float(obstacle_radius)
    if guidance_margin == 0.0:
        return (signed_clearance <= 0.0).to(dtype=z.dtype)
    gate = 1.0 - torch.clamp(signed_clearance / float(guidance_margin), min=0.0, max=1.0)
    return gate


def compute_multi_obstacle_distance_gate(
    z: torch.Tensor,
    obstacle_centers: torch.Tensor,
    obstacle_radii: torch.Tensor,
    guidance_margin: float,
) -> torch.Tensor:
    centers = obstacle_centers.to(device=z.device, dtype=z.dtype)
    radii = obstacle_radii.to(device=z.device, dtype=z.dtype).flatten()
    if centers.ndim != 2 or centers.shape[-1] != 3:
        raise ValueError(f"obstacle_centers must have shape (M, 3), got {tuple(centers.shape)}.")
    if radii.ndim != 1 or radii.shape[0] != centers.shape[0]:
        raise ValueError("obstacle_radii must have shape (M,) and match obstacle_centers.")
    if centers.shape[0] <= 0:
        raise ValueError("At least one obstacle is required.")

    gates = []
    for center, radius in zip(centers, radii):
        gates.append(
            compute_obstacle_distance_gate(
                z=z,
                obstacle_center=center,
                obstacle_radius=float(radius.item()),
                guidance_margin=guidance_margin,
            )
        )
    return torch.stack(gates, dim=0).amax(dim=0)


def guidance_strength(t_scalar: float, guidance_scale: float, guidance_decay: str) -> float:
    if guidance_decay in ("constant", "distance_gated"):
        return guidance_scale
    raise ValueError(f"Unsupported guidance_decay: {guidance_decay}")


def clip_guidance_norm(guidance: torch.Tensor, max_guidance_norm: float) -> torch.Tensor:
    if max_guidance_norm <= 0.0:
        return guidance
    norm = torch.linalg.norm(guidance, dim=-1, keepdim=True).clamp_min(1e-6)
    return guidance * torch.clamp(max_guidance_norm / norm, max=1.0)


@torch.no_grad()
def euler_sample(
    model: torch.nn.Module,
    num_samples: int,
    seq_len: int,
    point_dim: int,
    steps: int,
    device: torch.device,
    z_init: torch.Tensor | None = None,
) -> torch.Tensor:
    if steps <= 0:
        raise ValueError("steps must be positive.")
    if num_samples <= 0:
        raise ValueError("num_samples must be positive.")

    z = make_initial_noise(num_samples, seq_len, point_dim, device, z_init=z_init)
    dt = 1.0 / float(steps)

    for i in range(steps):
        t_scalar = i / float(steps)
        t = torch.full((num_samples, 1), t_scalar, device=device, dtype=torch.float32)
        v = model(z, t)
        z = z + v * dt
        if not torch.isfinite(z).all():
            raise RuntimeError(f"Non-finite values encountered during Euler step {i}.")
    return z


@torch.no_grad()
def conditional_euler_sample(
    model: torch.nn.Module,
    condition: torch.Tensor,
    num_samples: int,
    seq_len: int,
    point_dim: int,
    steps: int,
    device: torch.device,
    z_init: torch.Tensor | None = None,
) -> torch.Tensor:
    if steps <= 0:
        raise ValueError("steps must be positive.")
    if num_samples <= 0:
        raise ValueError("num_samples must be positive.")

    z = make_initial_noise(num_samples, seq_len, point_dim, device, z_init=z_init)
    condition_batch = prepare_condition_batch(condition, num_samples, device)
    dt = 1.0 / float(steps)

    for i in range(steps):
        t_scalar = i / float(steps)
        t = torch.full((num_samples, 1), t_scalar, device=device, dtype=torch.float32)
        v = model(z, t, condition_batch)
        z = z + v * dt
        if not torch.isfinite(z).all():
            raise RuntimeError(f"Non-finite values encountered during conditional Euler step {i}.")
    return z


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
    z_init: torch.Tensor | None = None,
    obstacle_centers: torch.Tensor | None = None,
    obstacle_radii: torch.Tensor | None = None,
) -> torch.Tensor:
    if steps <= 0:
        raise ValueError("steps must be positive.")
    if num_samples <= 0:
        raise ValueError("num_samples must be positive.")
    if point_dim != 3:
        raise ValueError("Energy guidance expects 3D trajectory points.")

    z = make_initial_noise(num_samples, seq_len, point_dim, device, z_init=z_init)
    dt = 1.0 / float(steps)
    centers = (
        obstacle_center.view(1, 3)
        if obstacle_centers is None
        else obstacle_centers.to(device=device, dtype=torch.float32)
    )
    radii = (
        torch.tensor([obstacle_radius], device=device, dtype=torch.float32)
        if obstacle_radii is None
        else obstacle_radii.to(device=device, dtype=torch.float32).flatten()
    )

    for i in range(steps):
        t_scalar = i / float(steps)
        t = torch.full((num_samples, 1), t_scalar, device=device, dtype=torch.float32)
        v = model(z, t)
        grad_e = compute_multi_obstacle_energy_gradient(
            z=z,
            obstacle_centers=centers,
            obstacle_radii=radii,
            guidance_margin=guidance_margin,
        )
        if guidance_decay == "distance_gated":
            gate = compute_multi_obstacle_distance_gate(
                z=z,
                obstacle_centers=centers,
                obstacle_radii=radii,
                guidance_margin=guidance_margin,
            )
            grad_e = grad_e * gate
        lambda_t = guidance_strength(t_scalar, guidance_scale, guidance_decay)
        guidance = clip_guidance_norm(lambda_t * grad_e, max_guidance_norm)
        z = z + (v - guidance) * dt
        if not torch.isfinite(z).all():
            raise RuntimeError(f"Non-finite values encountered during guided Euler step {i}.")
    return z


@torch.no_grad()
def conditional_guided_euler_sample(
    model: torch.nn.Module,
    condition: torch.Tensor,
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
    z_init: torch.Tensor | None = None,
    obstacle_centers: torch.Tensor | None = None,
    obstacle_radii: torch.Tensor | None = None,
) -> torch.Tensor:
    if steps <= 0:
        raise ValueError("steps must be positive.")
    if num_samples <= 0:
        raise ValueError("num_samples must be positive.")
    if point_dim != 3:
        raise ValueError("Energy guidance expects 3D trajectory points.")

    z = make_initial_noise(num_samples, seq_len, point_dim, device, z_init=z_init)
    condition_batch = prepare_condition_batch(condition, num_samples, device)
    dt = 1.0 / float(steps)
    centers = (
        obstacle_center.view(1, 3)
        if obstacle_centers is None
        else obstacle_centers.to(device=device, dtype=torch.float32)
    )
    radii = (
        torch.tensor([obstacle_radius], device=device, dtype=torch.float32)
        if obstacle_radii is None
        else obstacle_radii.to(device=device, dtype=torch.float32).flatten()
    )

    for i in range(steps):
        t_scalar = i / float(steps)
        t = torch.full((num_samples, 1), t_scalar, device=device, dtype=torch.float32)
        v = model(z, t, condition_batch)
        grad_e = compute_multi_obstacle_energy_gradient(
            z=z,
            obstacle_centers=centers,
            obstacle_radii=radii,
            guidance_margin=guidance_margin,
        )
        if guidance_decay == "distance_gated":
            gate = compute_multi_obstacle_distance_gate(
                z=z,
                obstacle_centers=centers,
                obstacle_radii=radii,
                guidance_margin=guidance_margin,
            )
            grad_e = grad_e * gate
        lambda_t = guidance_strength(t_scalar, guidance_scale, guidance_decay)
        guidance = clip_guidance_norm(lambda_t * grad_e, max_guidance_norm)
        z = z + (v - guidance) * dt
        if not torch.isfinite(z).all():
            raise RuntimeError(
                f"Non-finite values encountered during conditional guided Euler step {i}."
            )
    return z


def obstacle_distance_stats(
    trajectories: np.ndarray,
    obstacle_center: np.ndarray,
    obstacle_radius: float | np.ndarray,
) -> tuple[float, float, float]:
    if trajectories.ndim != 3 or trajectories.shape[-1] != 3:
        raise ValueError(f"Expected trajectories shape (N, T, 3), got {trajectories.shape}.")

    centers = np.asarray(obstacle_center, dtype=np.float32)
    if centers.ndim == 1:
        centers = centers.reshape(1, 3)
    if centers.ndim != 2 or centers.shape[-1] != 3:
        raise ValueError(f"Expected obstacle centers shape (3,) or (M, 3), got {centers.shape}.")
    radii = np.asarray(obstacle_radius, dtype=np.float32).reshape(-1)
    if radii.size == 1:
        radii = np.repeat(radii, centers.shape[0])
    if radii.shape[0] != centers.shape[0]:
        raise ValueError("obstacle_radius must be scalar or match the number of centers.")

    distances = np.linalg.norm(trajectories[:, :, None, :] - centers.reshape(1, 1, -1, 3), axis=-1)
    min_per_obstacle = distances.min(axis=1)
    collision_per_trajectory = np.any(min_per_obstacle <= radii.reshape(1, -1), axis=1)
    min_per_trajectory = min_per_obstacle.min(axis=1)
    collision_rate = float(np.mean(collision_per_trajectory))
    success_rate = 1.0 - collision_rate
    min_distance = float(min_per_trajectory.min())
    return collision_rate, success_rate, min_distance
