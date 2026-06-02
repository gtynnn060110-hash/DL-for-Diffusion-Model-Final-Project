import argparse
import numpy as np
from pathlib import Path

default_num_trajectories = 50
default_obstacle_radius = 1.0

def cubic_bezier(p0, p1, p2, p3, t):
    t = t.reshape(-1, 1)
    one_minus = 1.0 - t
    return (
        (one_minus**3) * p0
        + 3.0 * (one_minus**2) * t * p1
        + 3.0 * one_minus * (t**2) * p2
        + (t**3) * p3
    )

def sample_control_points(rng, min_clearance):
    y1 = rng.uniform(-3.5, 3.5)
    z1 = rng.uniform(1.5, 4.0) * rng.choice([-1.0, 1.0])
    y2 = rng.uniform(-3.5, 3.5)
    z2 = rng.uniform(1.5, 4.0) * rng.choice([-1.0, 1.0])

    p1 = np.array([-2.0, y1, z1], dtype=np.float32)
    p2 = np.array([2.0, y2, z2], dtype=np.float32)

    mid = 0.5 * (p1 + p2)
    if np.linalg.norm(mid[:2]) < min_clearance:
        p1[1] += np.sign(p1[1] + 1e-5) * min_clearance
        p2[1] += np.sign(p2[1] + 1e-5) * min_clearance

    return p1, p2

def is_collision_free(trajectory, obstacle_radius):
    distances = np.linalg.norm(trajectory, axis=1)
    return bool(np.all(distances > obstacle_radius))


def generate_trajectories_data(
    num_trajectories,
    seq_len,
    min_clearance,
    obstacle_radius,
    seed,
    max_attempts_per_trajectory=200,
):
    if num_trajectories <= 0:
        raise ValueError("num_trajectories must be positive.")
    if seq_len <= 1:
        raise ValueError("seq_len must be greater than 1.")
    if obstacle_radius < 0.0:
        raise ValueError("obstacle_radius must be non-negative.")
    if max_attempts_per_trajectory <= 0:
        raise ValueError("max_attempts_per_trajectory must be positive.")

    rng = np.random.default_rng(seed)
    t_vals = np.linspace(0.0, 1.0, seq_len, dtype=np.float32)

    p0 = np.array([-5.0, 0.0, 0.0], dtype=np.float32)
    p3 = np.array([5.0, 0.0, 0.0], dtype=np.float32)

    trajectories = np.zeros((num_trajectories, seq_len, 3), dtype=np.float32)
    rejected = 0
    for i in range(num_trajectories):
        for _ in range(max_attempts_per_trajectory):
            p1, p2 = sample_control_points(rng, min_clearance)
            trajectory = cubic_bezier(p0, p1, p2, p3, t_vals)
            if is_collision_free(trajectory, obstacle_radius):
                trajectories[i] = trajectory
                break
            rejected += 1
        else:
            raise RuntimeError(
                "Failed to generate a collision-free trajectory. "
                "Try reducing obstacle_radius or min_clearance, or increase max_attempts_per_trajectory."
            )

    return trajectories, rejected

def create_3d_plot(trajectories, obstacle_radius):
    import plotly.graph_objects as go

    fig = go.Figure()

    # 1. 绘制中心障碍物
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x = obstacle_radius * np.cos(u) * np.sin(v)
    y = obstacle_radius * np.sin(u) * np.sin(v)
    z = obstacle_radius * np.cos(v)

    fig.add_trace(go.Surface(
        x=x, y=y, z=z, colorscale='Reds', opacity=0.5, showscale=False, name="Obstacle"
    ))

    # 2. 绘制轨迹
    for i in range(trajectories.shape[0]):
        traj = trajectories[i]
        fig.add_trace(go.Scatter3d(
            x=traj[:, 0], y=traj[:, 1], z=traj[:, 2],
            mode='lines',
            line=dict(width=3, color='blue'),
            opacity=0.3,
            showlegend=False
        ))

    fig.add_trace(go.Scatter3d(x=[-5], y=[0], z=[0], mode='markers', marker=dict(size=8, color='green'), name="Start"))
    fig.add_trace(go.Scatter3d(x=[5], y=[0], z=[0], mode='markers', marker=dict(size=8, color='cyan'), name="Goal"))

    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[-6, 6]),
            yaxis=dict(range=[-6, 6]),
            zaxis=dict(range=[-6, 6]),
            aspectmode='cube'
        ),
        margin=dict(l=0, r=0, b=0, t=0)
    )
    return fig

CURRENT_DATA = None
CURRENT_GENERATION_INFO = {}

def update_plot(num, seq_len, min_clearance, obstacle_radius, seed):
    global CURRENT_DATA, CURRENT_GENERATION_INFO
    # 生成数据
    CURRENT_DATA, rejected = generate_trajectories_data(
        num_trajectories=int(num),
        seq_len=int(seq_len),
        min_clearance=min_clearance,
        obstacle_radius=obstacle_radius,
        seed=int(seed),
    )
    CURRENT_GENERATION_INFO = {
        "rejected": rejected,
        "obstacle_radius": obstacle_radius,
    }
    # 渲染图表
    fig = create_3d_plot(CURRENT_DATA, obstacle_radius)
    return (
        fig,
        "当前轨迹形状: "
        f"{CURRENT_DATA.shape} | 障碍物半径: {obstacle_radius:.2f} | "
        f"碰撞过滤丢弃候选轨迹数: {rejected}",
    )

def save_data(output_path):
    global CURRENT_DATA, CURRENT_GENERATION_INFO
    if CURRENT_DATA is None:
        return "请先生成数据！"
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    np.save(path, CURRENT_DATA)
    rejected = CURRENT_GENERATION_INFO.get("rejected", 0)
    return (
        f"成功保存 {CURRENT_DATA.shape} 形状的数据至: {output_path}。"
        f" 本次生成共过滤掉 {rejected} 条碰撞候选轨迹。"
    )

def build_demo():
    import gradio as gr

    with gr.Blocks(title="流匹配专家轨迹生成器") as demo:
        gr.Markdown("## Flow Matching 专家轨迹交互生成器")

        with gr.Row():
            with gr.Column(scale=1):
                num_slider = gr.Slider(10, 200, value=default_num_trajectories, step=10, label="轨迹数量 (N)")
                clearance_slider = gr.Slider(0.0, 5.0, value=1.5, step=0.1, label="轨迹避让距离 (Curvature)")
                radius_slider = gr.Slider(0.1, 3.0, value=1.0, step=0.1, label="中心障碍物半径 (可视化)")
                seq_len_slider = gr.Slider(10, 200, value=50, step=10, label="序列长度 (T)")
                seed_slider = gr.Slider(0, 1000, value=42, step=1, label="随机种子 (刷新形状)")

                out_path_text = gr.Textbox(value="dataset/toy_trajectories.npy", label="保存路径")
                save_btn = gr.Button("保存 NPY 数据集", variant="primary")
                status_text = gr.Textbox(label="系统状态", interactive=False)

            with gr.Column(scale=2):
                plot_output = gr.Plot(label="3D 轨迹预览 (可鼠标旋转缩放)")

        inputs = [num_slider, seq_len_slider, clearance_slider, radius_slider, seed_slider]
        for ctrl in inputs:
            ctrl.change(fn=update_plot, inputs=inputs, outputs=[plot_output, status_text])

        demo.load(fn=update_plot, inputs=inputs, outputs=[plot_output, status_text])
        save_btn.click(fn=save_data, inputs=[out_path_text], outputs=[status_text])

    return demo


def parse_args():
    parser = argparse.ArgumentParser(description="Flow Matching 专家轨迹生成器")
    parser.add_argument(
        "--visualize",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="是否启用可视化界面（默认启用）",
    )
    parser.add_argument("--num-trajectories", type=int, default=default_num_trajectories, help="生成轨迹数量 N")
    parser.add_argument("--seq-len", type=int, default=50, help="轨迹序列长度 T")
    parser.add_argument("--min-clearance", type=float, default=1.5, help="轨迹最小避让距离")
    parser.add_argument("--obstacle-radius", type=float, default=default_obstacle_radius, help="中心球形障碍物半径")
    parser.add_argument("--seed", type=int, default=42, help="随机种子")
    parser.add_argument(
        "--max-attempts-per-trajectory",
        type=int,
        default=200,
        help="每条轨迹最多重采样次数，用于碰撞过滤",
    )
    parser.add_argument("--output-path", type=str, default="dataset/toy_trajectories.npy", help="生成模式保存路径")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    if args.visualize:
        build_demo().launch(inbrowser=True)
    else:
        trajectories, rejected = generate_trajectories_data(
            num_trajectories=args.num_trajectories,
            seq_len=args.seq_len,
            min_clearance=args.min_clearance,
            obstacle_radius=args.obstacle_radius,
            seed=args.seed,
            max_attempts_per_trajectory=args.max_attempts_per_trajectory,
        )
        output_path = Path(args.output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        np.save(output_path, trajectories)
        print(
            f"已生成轨迹数据: {trajectories.shape} -> {output_path} | "
            f"障碍物半径={args.obstacle_radius:.2f} | "
            f"碰撞过滤丢弃候选轨迹数={rejected}"
        )
