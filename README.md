# 基于 Rectified Flow 的 3D 避障轨迹生成

本项目复现 **Rectified Flow** 在三维轨迹生成上的基本流程，并沿两条路线提升 OOD 障碍物场景下的避障成功率：

1. **推断期 Energy Guidance**：不重训模型，在采样时叠加障碍物排斥势能梯度（`constant` / `distance_gated`）
2. **训练期 Conditional Rectified Flow**：将障碍物参数作为条件输入，让速度场学习 `v_θ(x, t, c)`

两条路线可叠加使用（conditional + guided），是当前最强组合。

## 项目结构

```text
data_generator.py              # 无条件轨迹数据生成（Bezier 曲线 + 碰撞过滤）
generate_conditional_data.py   # 条件轨迹数据生成（含障碍物参数向量）
model.py                       # RectifiedFlowMLP + RectifiedFlowConditionalMLP
train.py / train_conditional.py # 训练脚本
flow_sampling.py               # 采样核心：Euler / Guided / Conditional 四种采样函数
recflow.py                     # Baseline 无条件推断 CLI
recflow_guided.py              # Energy-Guided 推断 CLI（constant / distance_gated）
recflow_conditional.py         # Conditional / Conditional+Guided 推断 CLI
evaluate.py                    # 批量评测（配对 z0，最多四路对比）
ablate_guidance.py             # 参数消融（支持 unconditional + conditional 四曲线对比）
visualize_trajectories.py      # 数据集浏览
```

## 方法概览

### Rectified Flow Baseline

训练速度场 `v_θ`，学习从高斯噪声到专家轨迹的直线路径：

```text
x_t = t · x1 + (1-t) · x0
L = MSE(v_θ(x_t, t), x1 - x0)
```

推断时用 Euler 积分：`z ← z + v_θ(z, t) · dt`

### Energy Guidance

不重训模型，在推断时注入障碍物排斥项：

```text
z ← z + (v_θ(z, t) - λ · ∇E(z)) · dt
```

两种模式：
- **constant**：全程恒定强度引导
- **distance_gated**：仅在障碍物 margin 范围内激活，远离障碍时自动减弱

### Conditional Rectified Flow

条件向量 `c` 为障碍物参数展平：`[cx1, cy1, cz1, r1, cx2, cy2, cz2, r2]`（`max_obstacles=2`，空位补 0）。模型学习 `v_θ(x, t, c)`，在推断时显式感知障碍物位置。

## 实验结果

### 无条件模型（200 样本，scale=3, margin=2, max_norm=10）

| Scenario | baseline | guided_constant | guided_distance_gated |
|----------|:--------:|:---------------:|:---------------------:|
| in_distribution_origin | 0.900 | 0.985 | **0.995** |
| ood_shifted_y | 0.855 | **1.000** | 0.995 |
| ood_double_gap | 0.615 | **0.970** | 0.930 |

- OOD 单障碍：guided 将成功率从 0.855 提升到 1.000
- OOD 双障碍：guided 将成功率从 0.615 提升到 0.970
- `distance_gated` 在成功率接近 `constant` 的同时，平滑度提升 50-60%，路径缩短 30-35%

### 条件模型四路对比（200 样本，distance_gated）

| Scenario | baseline | cond | guided_dg | cond+guided_dg |
|----------|:--------:|:----:|:---------:|:--------------:|
| in_distribution_origin | 0.750 | 0.745 | 0.980 | 0.975 |
| ood_shifted_y | 0.780 | 0.815 | **1.000** | **1.000** |
| ood_double_gap | 0.575 | 0.720 | 0.955 | **0.970** |

- 纯 conditional 在 OOD 场景优于无条件 baseline（双障碍 +14.5%），说明模型从障碍条件中学习到了避障行为
- **conditional + guided 是当前最强组合**：双障碍成功率 0.970，单障碍 1.000

### 消融实验（每个配置 500 样本）

完成 `guidance_scale` / `guidance_margin` / `max_guidance_norm` 三参数 sweep，同时对比 unconditional 和 conditional 各两条 guidance 曲线。关键发现：

- `guidance_scale=3.0` 是成功率与轨迹质量的平衡点
- `guidance_margin=2.0` 在 OOD 和双障碍场景下最稳健
- `max_guidance_norm` 在 6-8 后收益饱和
- 条件模型可在略低的 guidance 强度下达到同等成功率，印证训练期条件与推断期引导的互补效应

推荐默认参数：`scale=3.0, margin=2.0, max_norm=10.0, decay=distance_gated`

完整消融结果见 `outputs/ablation_guidance_summary_*.md` 和 `outputs/ablation_conditional_guidance_summary_*.md`。

## 运行方式

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 无条件管道

```bash
# 生成数据
python data_generator.py --no-visualize --num-trajectories 5000 --seq-len 50 --output-path dataset/toy_trajectories.npy

# 训练
python train.py --data-path dataset/toy_trajectories.npy --checkpoint-path checkpoints/rectified_flow_mlp.pt --epochs 200 --seed 42

# Baseline 推断
python recflow.py --checkpoint-path checkpoints/rectified_flow_mlp.pt --data-path dataset/toy_trajectories.npy --steps 20 --num-samples 50 --no-show

# Guided 推断（单障碍）
python recflow_guided.py --checkpoint-path checkpoints/rectified_flow_mlp.pt --data-path dataset/toy_trajectories.npy --steps 20 --num-samples 50 --obstacle-center 0 1.5 0 --obstacle-radius 1.0 --guidance-scale 3.0 --guidance-margin 2.0 --guidance-decay distance_gated --no-show

# Guided 推断（双障碍）
python recflow_guided.py --checkpoint-path checkpoints/rectified_flow_mlp.pt --data-path dataset/toy_trajectories.npy --steps 20 --num-samples 50 --obstacle 0 1.5 0 1.0 --obstacle 0 -1.5 0 1.0 --guidance-scale 3.0 --guidance-margin 2.0 --guidance-decay distance_gated --no-show

# 批量评测
python evaluate.py --device cpu

# 随机 OOD 评测
python evaluate.py --device cpu --random-ood-count 20

# 参数消融
python ablate_guidance.py --device cpu --ablate guidance_scale
```

### 3. 条件管道

```bash
# 生成条件数据
python generate_conditional_data.py --num-trajectories 5000 --seq-len 50 --max-obstacles 2 --output-path dataset/conditional_trajectories.npz

# 训练条件模型
python train_conditional.py --data-path dataset/conditional_trajectories.npz --checkpoint-path checkpoints/rectified_flow_conditional_mlp.pt --epochs 200 --seed 42

# 条件推断（无 guidance）
python recflow_conditional.py --checkpoint-path checkpoints/rectified_flow_conditional_mlp.pt --data-path dataset/conditional_trajectories.npz --num-samples 50 --steps 20 --obstacle-center 0 1.5 0 --obstacle-radius 1.0 --save-fig outputs/conditional_ood.png --no-show

# 条件 + guided 推断
python recflow_conditional.py --checkpoint-path checkpoints/rectified_flow_conditional_mlp.pt --data-path dataset/conditional_trajectories.npz --num-samples 50 --steps 20 --obstacle-center 0 1.5 0 --obstacle-radius 1.0 --guided --guidance-scale 3.0 --guidance-margin 2.0 --guidance-decay distance_gated --save-fig outputs/conditional_guided_ood.png --no-show

# 四路对比评测
python evaluate.py --device cpu --conditional-checkpoint-path checkpoints/rectified_flow_conditional_mlp.pt --guidance-decay distance_gated --output-json outputs/evaluation_conditional_results.json --output-markdown outputs/evaluation_conditional_summary.md

# 条件消融（四曲线对比）
python ablate_guidance.py --device cpu --conditional-checkpoint-path checkpoints/rectified_flow_conditional_mlp.pt --ablate guidance_scale --num-samples 500 --plot
```

Windows 上若遇到 `libiomp5md.dll already initialized`：

```powershell
$env:KMP_DUPLICATE_LIB_OK='TRUE'
```

## 文档索引

| 文档 | 用途 |
|------|------|
| [CLAUDE.md](CLAUDE.md) | 开发指南（命令、架构、设计决策） |
| [WORKLOG.md](WORKLOG.md) | 开发日志（里程碑、关键决策、教训） |
| [DEFENSE_NOTES.md](DEFENSE_NOTES.md) | 答辩叙事提纲 |

## 局限与下一步

- 障碍物支持静态球形软边界，尚未覆盖复杂几何或动态障碍
- Energy guidance 是推断期启发式，强引导会带来轨迹扭曲（`distance_gated` 缓解但不能消除）
- Conditional 模型使用简单拼接条件，尚未探索 CFG / SDF / occupancy 等更强条件机制
- 下一步计划：Classifier-Free Guidance 让条件模型内化避障行为
