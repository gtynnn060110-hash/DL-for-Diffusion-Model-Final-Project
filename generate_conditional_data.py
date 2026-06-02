import argparse
import json
from pathlib import Path

import numpy as np

from data_generator import cubic_bezier, sample_control_points


def validate_range(name: str, values: tuple[float, float] | list[float]) -> tuple[float, float]:
    lower, upper = float(values[0]), float(values[1])
    if lower > upper:
        raise ValueError(f"{name} lower bound must be <= upper bound.")
    return lower, upper


def sample_obstacles(
    rng: np.random.Generator,
    max_obstacles: int,
    obstacle_count: int,
    y_range: tuple[float, float],
    z_range: tuple[float, float],
    radius_range: tuple[float, float],
    min_center_norm: float,
    max_attempts: int = 1000,
) -> tuple[np.ndarray, np.ndarray]:
    if obstacle_count <= 0 or obstacle_count > max_obstacles:
        raise ValueError("obstacle_count must be in [1, max_obstacles].")

    y_min, y_max = y_range
    z_min, z_max = z_range
    r_min, r_max = radius_range
    centers: list[np.ndarray] = []
    radii: list[float] = []
    attempts = 0
    while len(centers) < obstacle_count and attempts < max_attempts:
        attempts += 1
        center = np.array(
            [0.0, rng.uniform(y_min, y_max), rng.uniform(z_min, z_max)],
            dtype=np.float32,
        )
        if np.linalg.norm(center) < min_center_norm:
            continue
        centers.append(center)
        radii.append(float(rng.uniform(r_min, r_max)))

    if len(centers) != obstacle_count:
        raise RuntimeError(
            f"Only sampled {len(centers)} obstacles after {max_attempts} attempts."
        )

    padded_centers = np.zeros((max_obstacles, 3), dtype=np.float32)
    padded_radii = np.zeros((max_obstacles,), dtype=np.float32)
    padded_centers[:obstacle_count] = np.stack(centers, axis=0)
    padded_radii[:obstacle_count] = np.asarray(radii, dtype=np.float32)
    return padded_centers, padded_radii


def make_condition(obstacle_centers: np.ndarray, obstacle_radii: np.ndarray) -> np.ndarray:
    if obstacle_centers.ndim != 2 or obstacle_centers.shape[1] != 3:
        raise ValueError("obstacle_centers must have shape (M, 3).")
    if obstacle_radii.ndim != 1 or obstacle_radii.shape[0] != obstacle_centers.shape[0]:
        raise ValueError("obstacle_radii must have shape (M,).")

    parts = []
    for center, radius in zip(obstacle_centers, obstacle_radii):
        parts.extend([float(center[0]), float(center[1]), float(center[2]), float(radius)])
    return np.asarray(parts, dtype=np.float32)


def is_collision_free_multi(
    trajectory: np.ndarray,
    obstacle_centers: np.ndarray,
    obstacle_radii: np.ndarray,
) -> bool:
    active = obstacle_radii > 0.0
    if not np.any(active):
        return True
    centers = obstacle_centers[active]
    radii = obstacle_radii[active]
    distances = np.linalg.norm(trajectory[:, None, :] - centers[None, :, :], axis=-1)
    return bool(np.all(distances > radii.reshape(1, -1)))


def generate_conditional_trajectories(
    num_trajectories: int,
    seq_len: int,
    min_clearance: float,
    max_obstacles: int,
    min_obstacles: int,
    max_active_obstacles: int,
    y_range: tuple[float, float],
    z_range: tuple[float, float],
    radius_range: tuple[float, float],
    min_center_norm: float,
    seed: int,
    max_attempts_per_trajectory: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    if num_trajectories <= 0:
        raise ValueError("num_trajectories must be positive.")
    if seq_len <= 1:
        raise ValueError("seq_len must be greater than 1.")
    if max_obstacles <= 0:
        raise ValueError("max_obstacles must be positive.")
    if min_obstacles <= 0 or min_obstacles > max_active_obstacles:
        raise ValueError("min_obstacles must be in [1, max_active_obstacles].")
    if max_active_obstacles > max_obstacles:
        raise ValueError("max_active_obstacles cannot exceed max_obstacles.")
    if max_attempts_per_trajectory <= 0:
        raise ValueError("max_attempts_per_trajectory must be positive.")

    rng = np.random.default_rng(seed)
    t_vals = np.linspace(0.0, 1.0, seq_len, dtype=np.float32)
    p0 = np.array([-5.0, 0.0, 0.0], dtype=np.float32)
    p3 = np.array([5.0, 0.0, 0.0], dtype=np.float32)

    trajectories = np.zeros((num_trajectories, seq_len, 3), dtype=np.float32)
    obstacle_centers = np.zeros((num_trajectories, max_obstacles, 3), dtype=np.float32)
    obstacle_radii = np.zeros((num_trajectories, max_obstacles), dtype=np.float32)
    conditions = np.zeros((num_trajectories, max_obstacles * 4), dtype=np.float32)
    obstacle_counts = np.zeros((num_trajectories,), dtype=np.int64)
    for i in range(num_trajectories):
        count = int(rng.integers(min_obstacles, max_active_obstacles + 1))
        centers, radii = sample_obstacles(
            rng=rng,
            max_obstacles=max_obstacles,
            obstacle_count=count,
            y_range=y_range,
            z_range=z_range,
            radius_range=radius_range,
            min_center_norm=min_center_norm,
        )

        for _ in range(max_attempts_per_trajectory):
            p1, p2 = sample_control_points(rng, min_clearance)
            trajectory = cubic_bezier(p0, p1, p2, p3, t_vals)
            if is_collision_free_multi(trajectory, centers, radii):
                trajectories[i] = trajectory
                obstacle_centers[i] = centers
                obstacle_radii[i] = radii
                conditions[i] = make_condition(centers, radii)
                obstacle_counts[i] = count
                break
        else:
            raise RuntimeError(
                "Failed to generate a collision-free conditional trajectory. "
                "Try increasing min_clearance, reducing obstacle radii, or increasing attempts."
            )

    return trajectories, conditions, obstacle_centers, obstacle_radii, obstacle_counts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate conditional trajectory data with per-sample obstacle parameters."
    )
    parser.add_argument("--num-trajectories", type=int, default=5000)
    parser.add_argument("--seq-len", type=int, default=50)
    parser.add_argument("--min-clearance", type=float, default=1.5)
    parser.add_argument("--max-obstacles", type=int, default=2)
    parser.add_argument("--min-obstacles", type=int, default=1)
    parser.add_argument("--max-active-obstacles", type=int, default=2)
    parser.add_argument("--obstacle-y-range", type=float, nargs=2, default=(-2.5, 2.5))
    parser.add_argument("--obstacle-z-range", type=float, nargs=2, default=(-1.5, 1.5))
    parser.add_argument("--obstacle-radius-range", type=float, nargs=2, default=(0.8, 1.2))
    parser.add_argument("--min-center-norm", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-attempts-per-trajectory", type=int, default=500)
    parser.add_argument("--output-path", type=str, default="dataset/conditional_trajectories.npz")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    y_range = validate_range("obstacle_y_range", args.obstacle_y_range)
    z_range = validate_range("obstacle_z_range", args.obstacle_z_range)
    radius_range = validate_range("obstacle_radius_range", args.obstacle_radius_range)
    if radius_range[0] < 0.0:
        raise ValueError("obstacle radius lower bound must be non-negative.")

    (
        trajectories,
        conditions,
        obstacle_centers,
        obstacle_radii,
        obstacle_counts,
    ) = generate_conditional_trajectories(
        num_trajectories=int(args.num_trajectories),
        seq_len=int(args.seq_len),
        min_clearance=float(args.min_clearance),
        max_obstacles=int(args.max_obstacles),
        min_obstacles=int(args.min_obstacles),
        max_active_obstacles=int(args.max_active_obstacles),
        y_range=y_range,
        z_range=z_range,
        radius_range=radius_range,
        min_center_norm=float(args.min_center_norm),
        seed=int(args.seed),
        max_attempts_per_trajectory=int(args.max_attempts_per_trajectory),
    )

    output_path = Path(args.output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "seed": int(args.seed),
        "seq_len": int(args.seq_len),
        "max_obstacles": int(args.max_obstacles),
        "min_obstacles": int(args.min_obstacles),
        "max_active_obstacles": int(args.max_active_obstacles),
        "condition_dim": int(args.max_obstacles) * 4,
        "obstacle_y_range": [float(v) for v in y_range],
        "obstacle_z_range": [float(v) for v in z_range],
        "obstacle_radius_range": [float(v) for v in radius_range],
        "min_center_norm": float(args.min_center_norm),
    }
    np.savez_compressed(
        output_path,
        trajectories=trajectories,
        conditions=conditions,
        obstacle_centers=obstacle_centers,
        obstacle_radii=obstacle_radii,
        obstacle_counts=obstacle_counts,
        metadata=json.dumps(metadata),
    )
    print(
        f"Saved conditional data: trajectories={trajectories.shape}, "
        f"conditions={conditions.shape} -> {output_path}"
    )


if __name__ == "__main__":
    main()
