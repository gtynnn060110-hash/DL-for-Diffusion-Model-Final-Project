import argparse
from pathlib import Path
from typing import Optional

import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Visualize 3D trajectories.")
    parser.add_argument("--data", type=str, default="dataset/toy_trajectories.npy", help="Path to .npy data file.")
    parser.add_argument("--max", type=int, default=20, help="Max number of trajectories to plot.")
    parser.add_argument("--save", type=str, default="", help="Optional path to save the figure.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_path = Path(args.data)
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")

    data = np.load(data_path)
    if data.ndim != 3 or data.shape[-1] != 3:
        raise ValueError("Expected data with shape (N, T, 3)")

    max_count = min(args.max, data.shape[0])

    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection="3d")

    for i in range(max_count):
        traj = data[i]
        ax.plot(traj[:, 0], traj[:, 1], traj[:, 2], alpha=0.8, linewidth=1.5)

    # Mark the start, end, and obstacle.
    ax.scatter([-5.0], [0.0], [0.0], color="green", s=50, label="start")
    ax.scatter([5.0], [0.0], [0.0], color="red", s=50, label="end")
    ax.scatter([0.0], [0.0], [0.0], color="black", s=40, label="obstacle")

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_title(f"Trajectories (showing {max_count}/{data.shape[0]})")
    ax.legend(loc="upper left")

    if args.save:
        output_path: Optional[Path] = Path(args.save)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
    else:
        plt.show()


if __name__ == "__main__":
    main()
