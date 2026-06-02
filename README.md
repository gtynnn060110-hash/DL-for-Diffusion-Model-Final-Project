# 基于能量引导流匹配的 3D 避障轨迹生成

本项目复现 `Rectified Flow` 在三维轨迹生成上的基本流程，并在推断阶段加入 `Energy Guidance`，用于提升新障碍物设置下的避障成功率。

核心思路是：先训练一个从高斯噪声生成平滑轨迹的速度场模型，再在采样时叠加球形障碍物的软排斥势能梯度。`recflow.py` 和 `recflow_guided.py` 使用同一个 checkpoint，区别只在推断更新公式；二者共用 [`flow_sampling.py`](flow_sampling.py) 中的采样实现。

## 项目结构

```text
data_generator.py         # 生成 3D Bezier 专家轨迹，并用中心球障碍物做碰撞过滤
generate_conditional_data.py # 生成带障碍条件向量的条件轨迹数据
visualize_trajectories.py # 可视化 .npy 轨迹数据
model.py                  # Unconditional / Conditional Rectified Flow MLP 与时间嵌入
train.py                  # 训练速度场 v_theta(x_t, t)
train_conditional.py      # 训练带障碍条件输入的速度场 v_theta(x_t, t, c)
flow_sampling.py          # 共享：Euler / Guided 采样、势能梯度、障碍统计、checkpoint 加载
recflow.py                # baseline 推断 CLI 与可视化（调用 flow_sampling）
recflow_guided.py         # Energy-Guided 推断 CLI 与可视化（调用 flow_sampling）
recflow_conditional.py    # Conditional / Conditional+Guided 推断 CLI 与可视化
evaluate.py               # 批量评测 baseline 和 guided（配对初始噪声 z0）
ablate_guidance.py        # guidance_scale / margin / norm 消融与 Pareto CSV / 图
PROJECT_PROGRESS.md       # 分阶段工作梳理（汇报 / 答辩用）
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
| `compute_obstacle_energy_gradient` | 单球 / 多球软边界排斥梯度 |
| `obstacle_distance_stats` | 单障碍 / 多障碍碰撞率、成功率、最小距离 |
| `load_model_from_checkpoint` | 加载训练 checkpoint |
| `set_seed` / `load_real_data` | 评测与 CLI 共用工具函数 |

**配对采样**：`evaluate.py` 对每个评测场景只采样一次 `z0`，baseline 与 guided 分别传入 `z_init` 与 `z_init.clone()`，保证二者差异仅来自 energy guidance，而非不同随机初值。

Phase 1 已在本模块上完成 `distance_gated` 自适应引导、多障碍势能叠加、随机 OOD 评测与 guidance 参数消融；CLI 脚本只负责参数解析和可视化。

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
- 多障碍输入：重复传入 `--obstacle X Y Z R`
- 引导强度：`--guidance-scale`
- 安全边界：`--guidance-margin`
- 引导模式：`--guidance-decay {constant, distance_gated}`
- 引导范数裁剪：`--max-guidance-norm`

## 当前实验结果

标准评测配置：

- 数据：`dataset/toy_trajectories.npy`
- Checkpoint：`checkpoints/rectified_flow_mlp.pt`
- 样本数：`200`
- 采样步数：`20`
- 随机种子：`42`
- Guidance：`scale=3.0, margin=2.0, decay in {constant, distance_gated}, max_norm=10.0`

`evaluate.py` 的一次 CPU 评测结果如下：

| Scenario | Method | Success Rate | Collision Rate | Min Distance | Smoothness | Path Length | Time (s) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| in_distribution_origin | baseline | 0.7500 | 0.2500 | 0.0847 | 0.2620 | 17.2844 | 0.0166 |
| in_distribution_origin | guided_constant | 0.9800 | 0.0200 | 0.6567 | 5.0614 | 55.9591 | 0.0148 |
| in_distribution_origin | guided_distance_gated | 0.9800 | 0.0200 | 0.6033 | 2.3036 | 38.8434 | 0.0159 |
| ood_shifted_y | baseline | 0.7800 | 0.2200 | 0.1062 | 0.2620 | 17.2844 | 0.0116 |
| ood_shifted_y | guided_constant | 1.0000 | 0.0000 | 1.4181 | 0.5978 | 22.3192 | 0.0149 |
| ood_shifted_y | guided_distance_gated | 1.0000 | 0.0000 | 1.0205 | 0.4709 | 20.2886 | 0.0158 |
| ood_double_gap | baseline | 0.5750 | 0.4250 | 0.0609 | 0.2620 | 17.2844 | 0.0123 |
| ood_double_gap | guided_constant | 0.9700 | 0.0300 | 0.8065 | 5.2318 | 54.6563 | 0.0160 |
| ood_double_gap | guided_distance_gated | 0.9550 | 0.0450 | 0.7946 | 1.9563 | 34.8642 | 0.0186 |

结果说明：

- 在 OOD 障碍物位置 `(0, 1.5, 0)` 下，两种 guided 方法都将成功率从 `0.7800` 提升到 `1.0000`。
- 在双障碍 `ood_double_gap` 场景下，baseline 成功率为 `0.5750`，guided 方法提升到 `0.9700` / `0.9550`。
- `guided_constant` 避障最强，但在 ID 和双障碍场景下路径更长、平滑度代价更高；`guided_distance_gated` 成功率接近，同时更平滑、更短。

完整评测输出见：

- `outputs/evaluation_summary.md`
- `outputs/evaluation_results.json`
- `outputs/base_ood.png`
- `outputs/guided_constant_ood.png`
- `outputs/guided_distance_gated_ood.png`
- `outputs/base_double_ood.png`
- `outputs/guided_constant_double_ood.png`
- `outputs/guided_distance_gated_double_ood.png`
- `outputs/ablation_guidance_summary_*.md`
- `outputs/ablation_plots/*.png`
- `outputs/evaluation_conditional_summary.md`
- `outputs/conditional_ood.png`
- `outputs/conditional_guided_ood.png`

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
python recflow_guided.py --checkpoint-path checkpoints/rectified_flow_mlp.pt --data-path dataset/toy_trajectories.npy --seed 42 --steps 20 --num-samples 50 --obstacle-center 0 1.5 0 --obstacle-radius 1.0 --guidance-scale 3.0 --guidance-margin 2.0 --guidance-decay constant --max-guidance-norm 10.0 --save-generated outputs/guided_constant_ood.npy --save-fig outputs/guided_constant_ood.png --no-show
```

### 6. 批量评测（配对 z0）

```bash
python evaluate.py --device cpu
```

`evaluate.py` 通过 `flow_sampling.make_initial_noise` 为每个场景生成一份 `z0`，baseline 与 guided 共用该初值进行公平对比。

### 7. Guidance 消融

```bash
python ablate_guidance.py --device cpu --ablate guidance_scale --num-samples 500
python ablate_guidance.py --device cpu --ablate guidance_margin --num-samples 500
python ablate_guidance.py --device cpu --ablate max_guidance_norm --num-samples 500
```

消融结果会写入 `outputs/ablation_guidance_summary_*.md`、`outputs/ablation_guidance_pareto_*.csv` 与 `outputs/ablation_plots/`。

加入 conditional checkpoint 后，同一脚本会额外输出 `conditional` 与 `conditional_<guidance_decay>`：

```bash
python ablate_guidance.py --device cpu --conditional-checkpoint-path checkpoints/rectified_flow_conditional_mlp.pt --ablate guidance_scale --num-samples 500 --output-json outputs/ablation_conditional_guidance_results.json --output-markdown outputs/ablation_conditional_guidance_summary.md --output-csv outputs/ablation_conditional_guidance_pareto.csv --plot
```

默认会同时 sweep `constant` 与 `distance_gated`，每张图包含 4 条曲线：`constant`、`distance_gated`、`cond_constant`、`cond_distance_gated`。表格中仍保留 `baseline` 与 `conditional` 参考行。

### 8. Conditional Rectified Flow（Phase 2）

```bash
python generate_conditional_data.py --num-trajectories 5000 --seq-len 50 --max-obstacles 2 --min-obstacles 1 --max-active-obstacles 2 --output-path dataset/conditional_trajectories.npz
python train_conditional.py --data-path dataset/conditional_trajectories.npz --checkpoint-path checkpoints/rectified_flow_conditional_mlp.pt --epochs 200 --seed 42
python evaluate.py --device cpu --conditional-checkpoint-path checkpoints/rectified_flow_conditional_mlp.pt --guidance-decay distance_gated --output-json outputs/evaluation_conditional_results.json --output-markdown outputs/evaluation_conditional_summary.md
```

Conditional 模型把障碍物编码为固定长度条件向量：每个球形障碍占 4 维 `(cx, cy, cz, radius)`，按 `max_obstacles` 展平，不足部分补 0。传入 `--conditional-checkpoint-path` 后，`evaluate.py` 会追加 `conditional` 与 `conditional_guided_*`，从而形成 `uncond / uncond+guided / cond / cond+guided` 四路对比；若只想严格四路，可只传一个 `--guidance-decay`。

可视化 conditional 采样效果：

```bash
python recflow_conditional.py --device cpu --num-samples 50 --steps 20 --obstacle-center 0 1.5 0 --obstacle-radius 1.0 --save-fig outputs/conditional_ood.png --save-generated outputs/conditional_ood.npy --no-show
python recflow_conditional.py --device cpu --num-samples 50 --steps 20 --obstacle-center 0 1.5 0 --obstacle-radius 1.0 --guided --save-fig outputs/conditional_guided_ood.png --save-generated outputs/conditional_guided_ood.npy --no-show
```

当前 200 样本四路对比中，`ood_shifted_y` 下 `conditional` 成功率为 `0.8150`，高于 uncond baseline 的 `0.7800`；`conditional_guided_distance_gated` 成功率为 `1.0000`，并将最小距离提升到 `1.3255`。在 `ood_double_gap` 下，`conditional` 成功率为 `0.7200`，高于 baseline 的 `0.5750`；`conditional_guided_distance_gated` 达到 `0.9700`。

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
5. 消融实验说明 guidance 参数存在成功率与轨迹质量的 trade-off，`distance_gated` 是更稳妥的默认展示配置。
6. 当前方法仍是推断期启发式引导，后续可扩展为条件 Flow Matching 或 SDF 条件输入。

更详细的答辩提纲见 `DEFENSE_NOTES.md`；分阶段工作与实验证据见 [`PROJECT_PROGRESS.md`](PROJECT_PROGRESS.md)。

## 局限与下一步

- 当前障碍物支持静态单球 / 多球软边界，尚未支持复杂几何或动态障碍物。
- 当前 guidance 不参与训练，强引导可能带来轨迹变长或平滑性下降；`distance_gated` 能缓解但不能完全消除这个 trade-off。
- 当前模型是整段轨迹 MLP，尚未引入更强的序列架构。
- Phase 2 已加入球形障碍参数条件输入；后续更合理的方向是扩展到 SDF、occupancy 或更强序列模型。

### Phase 1 进度

- [x] Step 1–2：`flow_sampling.py` + 脚本瘦身 + `evaluate.py` 配对 `z0`
- [x] Step 3：`distance_gated` 自适应引导
- [x] Step 4：多障碍势能叠加 + 双球夹缝 demo
- [x] Step 5/6：固定与随机 OOD 评测
- [x] Step 7：guidance 参数消融、Pareto CSV 与图

### Phase 2 进度

- [x] 条件数据生成脚本：`generate_conditional_data.py`
- [x] `RectifiedFlowConditionalMLP` + `train_conditional.py`
- [x] `evaluate.py` 支持四路对比接口
- [x] `recflow_conditional.py` 支持 conditional / conditional+guided 可视化
- [x] `ablate_guidance.py` 支持 conditional guidance ablation 接口
- [x] 跑完 conditional 训练与 200 样本四路评测
- [ ] 进一步调参或扩展到更强条件表示（如 SDF）
