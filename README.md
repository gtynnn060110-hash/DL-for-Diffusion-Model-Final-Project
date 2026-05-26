# 基于能量引导流匹配的 3D 避障轨迹生成

本项目复现 `Rectified Flow` 在三维轨迹生成上的基本流程，并在推断阶段加入 `Energy Guidance`，用于提升新障碍物设置下的避障成功率。

核心思路是：先训练一个从高斯噪声生成平滑轨迹的速度场模型，再在采样时叠加球形障碍物的软排斥势能梯度。`recflow.py` 和 `recflow_guided.py` 使用同一个 checkpoint，区别只在推断更新公式；二者共用 [`flow_sampling.py`](flow_sampling.py) 中的采样实现。

## 项目结构

```text
data_generator.py         # 生成 3D Bezier 专家轨迹，并用中心球障碍物做碰撞过滤
visualize_trajectories.py # 可视化 .npy 轨迹数据
model.py                  # Rectified Flow MLP 与时间嵌入
train.py                  # 训练速度场 v_theta(x_t, t)
flow_sampling.py          # 共享：Euler / Guided 采样、势能梯度、障碍统计、checkpoint 加载
recflow.py                # baseline 推断 CLI 与可视化（调用 flow_sampling）
recflow_guided.py         # Energy-Guided 推断 CLI 与可视化（调用 flow_sampling）
evaluate.py               # 批量评测 baseline 和 guided（配对初始噪声 z0）
DEFENSE_NOTES.md          # 答辩叙事提纲
```

## 采样模块（Phase 1）

[`flow_sampling.py`](flow_sampling.py) 集中实现推断期的核心逻辑，避免 `recflow.py` / `recflow_guided.py` / `evaluate.py` 各维护一份采样代码。

主要 API：

| 函数 | 作用 |
| --- | --- |
| `make_initial_noise(..., z_init=None)` | 生成或校验初始噪声 `z0` |
| `euler_sample(..., z_init=None)` | Baseline：`z ← z + v_θ(z,t)·dt` |
| `guided_euler_sample(..., z_init=None)` | Guided：`z ← z + (v_θ - λ·∇E)·dt` |
| `compute_obstacle_energy_gradient` | 单球软边界排斥梯度 |
| `obstacle_distance_stats` | 碰撞率 / 成功率 / 最小距离 |
| `load_model_from_checkpoint` | 加载训练 checkpoint |
| `set_seed` / `load_real_data` | 评测与 CLI 共用工具函数 |

**配对采样**：`evaluate.py` 对每个评测场景只采样一次 `z0`，baseline 与 guided 分别传入 `z_init` 与 `z_init.clone()`，保证二者差异仅来自 energy guidance，而非不同随机初值。

后续 Phase 1 步骤（自适应 `distance_gated`、多障碍、随机 OOD 评测）将直接扩展本模块，无需再改 CLI 脚本的积分循环。

## 方法概览

### 1. 数据生成

`data_generator.py` 生成形状为 `(N, T, 3)` 的专家轨迹数据。当前场景固定起点 `(-5, 0, 0)` 和终点 `(5, 0, 0)`，中间轨迹由三次 Bezier 曲线生成，并过滤掉与原点球形障碍物碰撞的候选轨迹。

### 2. Rectified Flow Baseline

`train.py` 读取专家轨迹 `x1`，采样高斯噪声 `x0`，在二者之间构造插值状态：

```text
x_t = t * x1 + (1 - t) * x0
v_target = x1 - x0
```

模型学习速度场 `v_theta(x_t, t)`。推断时，`recflow.py` 从高斯噪声出发，用 Euler 方法生成完整轨迹：

```text
x = x + v_theta(x, t) * dt
```

### 3. Energy-Guided Inference

`recflow_guided.py` 不重新训练模型，而是在推断时加入球形障碍物的排斥项：

```text
x = x + (v_theta(x, t) - lambda_t * grad E(x)) * dt
```

其中 `E(x)` 是障碍物附近的软边界势能。当前实现支持：

- 障碍物中心：`--obstacle-center`
- 障碍物半径：`--obstacle-radius`
- 引导强度：`--guidance-scale`
- 安全边界：`--guidance-margin`
- 时间衰减：`--guidance-decay {constant, linear}`
- 引导范数裁剪：`--max-guidance-norm`

## 当前实验结果

标准评测配置：

- 数据：`dataset/toy_trajectories.npy`
- Checkpoint：`checkpoints/rectified_flow_mlp.pt`
- 样本数：`200`
- 采样步数：`20`
- 随机种子：`42`
- Guidance：`scale=3.0, margin=2.0, decay=constant, max_norm=10.0`

`evaluate.py` 的一次 CPU 评测结果如下：

| Scenario | Method | Success Rate | Collision Rate | Min Distance | Smoothness | Path Length | Time (s) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| in_distribution_origin | baseline | 0.9000 | 0.1000 | 0.1206 | 0.3040 | 18.1034 | 0.1952 |
| in_distribution_origin | guided | 0.9850 | 0.0150 | 0.6177 | 4.4957 | 53.0077 | 0.1102 |
| ood_shifted_y | baseline | 0.8550 | 0.1450 | 0.1298 | 0.3040 | 18.1034 | 0.0512 |
| ood_shifted_y | guided | 1.0000 | 0.0000 | 1.4554 | 0.5742 | 22.3743 | 0.1112 |

结果说明：

- 在 OOD 障碍物位置 `(0, 1.5, 0)` 下，guided 将成功率从 `0.8550` 提升到 `1.0000`。
- Guided 的最小障碍物距离明显提高，说明排斥势能确实改变了危险轨迹。
- 强 guidance 在训练内原点障碍场景下会显著拉长路径并降低平滑性，因此更适合作为 OOD 推断期修正，而不是无条件替代 baseline。

完整评测输出见：

- `outputs/evaluation_summary.md`
- `outputs/evaluation_results.json`
- `outputs/base_ood.png`
- `outputs/guided_ood.png`

## 运行方式

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 生成训练数据

```bash
python data_generator.py --no-visualize --num-trajectories 5000 --seq-len 50 --obstacle-radius 1.0 --output-path dataset/toy_trajectories.npy
```

### 3. 训练模型

```bash
python train.py --data-path dataset/toy_trajectories.npy --checkpoint-path checkpoints/rectified_flow_mlp.pt --epochs 200 --seed 42
```

### 4. Baseline 推断

```bash
python recflow.py --checkpoint-path checkpoints/rectified_flow_mlp.pt --data-path dataset/toy_trajectories.npy --seed 42 --steps 20 --num-samples 50 --obstacle-center 0 1.5 0 --obstacle-radius 1.0 --save-generated outputs/base_ood.npy --save-fig outputs/base_ood.png --no-show
```

### 5. Energy-Guided 推断

```bash
python recflow_guided.py --checkpoint-path checkpoints/rectified_flow_mlp.pt --data-path dataset/toy_trajectories.npy --seed 42 --steps 20 --num-samples 50 --obstacle-center 0 1.5 0 --obstacle-radius 1.0 --guidance-scale 3.0 --guidance-margin 2.0 --guidance-decay constant --max-guidance-norm 10.0 --save-generated outputs/guided_ood.npy --save-fig outputs/guided_ood.png --no-show
```

### 6. 批量评测（配对 z0）

```bash
python evaluate.py --device cpu
```

`evaluate.py` 通过 `flow_sampling.make_initial_noise` 为每个场景生成一份 `z0`，baseline 与 guided 共用该初值进行公平对比。

如果 Windows 环境中出现 `libiomp5md.dll already initialized`，可临时使用：

```powershell
$env:KMP_DUPLICATE_LIB_OK='TRUE'
python evaluate.py --device cpu
```

## 答辩重点

推荐围绕以下主线讲述：

1. Rectified Flow 能用较少步数从噪声生成完整轨迹。
2. Baseline 学到的是训练数据分布，不显式感知新的障碍物位置。
3. Energy Guidance 在不重训模型的前提下，用物理排斥势能修正推断轨迹。
4. OOD 障碍物实验显示 guided 能显著提高避障成功率。
5. 当前方法仍是推断期启发式引导，后续可扩展为条件 Flow Matching 或 SDF 条件输入。

更详细的答辩提纲见 `DEFENSE_NOTES.md`。

## 局限与下一步

- 当前障碍物只支持球形软边界，尚未支持复杂几何、多障碍或动态障碍物。
- 当前 guidance 不参与训练，强引导可能带来轨迹变长或平滑性下降；Phase 1 后续将加入 `distance_gated` 等自适应引导以缓解 in-distribution 副作用。
- 当前模型是整段轨迹 MLP，尚未引入更强的序列架构。
- 后续更合理的方向是把障碍物参数或 SDF 表示作为条件输入，训练 conditional Rectified Flow（Phase 2）。

### Phase 1 进度

- [x] Step 1–2：`flow_sampling.py` + 脚本瘦身 + `evaluate.py` 配对 `z0`
- [ ] Step 3–7：自适应引导、多障碍、随机 OOD 评测、消融与文档