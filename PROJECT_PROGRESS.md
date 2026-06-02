# 项目进展梳理（PROJECT_PROGRESS）

> 本文档用于**阶段汇报 / 答辩准备**，按时间线记录「要解决什么 → 做了什么 → 证明了什么 → 还有什么问题」。  
> 使用说明与命令见 [README.md](README.md)；答辩话术见 [DEFENSE_NOTES.md](DEFENSE_NOTES.md)。

---

## 一句话定位

在 3D 轨迹生成任务上复现 **Rectified Flow**，并用两条路线提升新障碍物（OOD）场景下的避障成功率：推断期 **Energy Guidance** 与训练期 **Conditional Rectified Flow**；当前已完成工程化采样、公平评测协议、`distance_gated` 自适应引导、多障碍 / 随机 OOD 评估、guidance 参数消融与 conditional 初版四路对比。

---

## 技术路线总览

```mermaid
flowchart LR
  subgraph done [已完成]
    A[data_generator] --> B[train_baseline]
    B --> C[recflow_baseline]
    C --> D[recflow_guided]
    D --> E[evaluate_batch]
    E --> F[flow_sampling_refactor]
    F --> G[adaptive_guidance]
    G --> H[multi_obstacle_eval]
    H --> I[random_OOD_eval]
    I --> J[guidance_ablation]
  end
  subgraph done2 [已完成初版]
    J --> K[conditional_RF]
  end
```

---

## 里程碑一览

| 阶段 | 状态 | 核心交付 | 关键文件 |
|------|------|----------|----------|
| **阶段一**：Baseline 框架 | 已完成 | 数据 → 训练 → 推断 → 可视化闭环 | `data_generator.py`, `model.py`, `train.py`, `recflow.py` |
| **阶段二**：Energy Guidance | 已完成 | 推断期势能引导 + 批量对比评测 | `recflow_guided.py`, `evaluate.py` |
| **阶段三**：采样模块化与公平评测 | 已完成 | `flow_sampling.py`、配对 `z0`、`evaluate` 更新 | `flow_sampling.py`, `evaluate.py` |
| Phase 1 Step 3 | 已完成 | `distance_gated` 自适应引导 + 三方法统一评估 | `flow_sampling.py`, `evaluate.py`, `recflow_guided.py` |
| Phase 1 Step 4 | 已完成 | 多障碍势能叠加 + 双球夹缝 demo | `flow_sampling.py`, `evaluate.py`, `recflow_guided.py` |
| Phase 1 Step 5/6 | 已完成 | 固定 / 随机 OOD 场景评估 + 均值汇总 | `evaluate.py` |
| Phase 1 Step 7 | 已完成 | guidance 参数消融 + Pareto CSV / 图 | `ablate_guidance.py`, `outputs/ablation_*` |
| Phase 2 | 已完成初版 | 条件化 Rectified Flow + 四路评测 + 可视化 + conditional ablation 接口 | `generate_conditional_data.py`, `train_conditional.py`, `recflow_conditional.py`, `evaluate.py`, `ablate_guidance.py` |

---

## 阶段一：搭建整体框架，实现 Rectified Flow Baseline

### 要解决的问题

- 课程项目需要完整复现 **1-Rectified Flow**：从高斯噪声生成与专家数据同分布的 3D 避障轨迹。
- 场景需可解释：固定起终点、中心球形障碍，轨迹由 Bezier 专家策略生成。

### 实现内容

| 模块 | 作用 |
|------|------|
| `data_generator.py` | 三次 Bezier 专家轨迹；过滤与原点障碍 `(0,0,0)` 碰撞的样本；输出 `(N, T, 3)` |
| `model.py` | `RectifiedFlowMLP`：轨迹展平 + 正弦时间嵌入，预测速度场 `v_θ(x_t, t)` |
| `train.py` | 插值 `x_t = t·x1 + (1-t)·x0`，损失 `MSE(v_θ, x1-x0)`；保存 checkpoint |
| `recflow.py` | Euler 采样：`z ← z + v_θ·dt`；3D 对比可视化 |
| `visualize_trajectories.py` | 数据集浏览 |

训练目标（与 `agent.md` 一致）：

```text
x_t = t * x1 + (1 - t) * x0
L = MSE(v_theta(x_t, t), x1 - x0)
```

### 验收与结论

- 能从 checkpoint 生成与专家轨迹形态相近的平滑曲线。
- **局限（为阶段二埋伏笔）**：模型只学习训练分布（障碍在原点），推断时**不显式输入**障碍物位置；换障碍后可能穿障。

### 常用命令

```bash
python data_generator.py --no-visualize --num-trajectories 5000 --seq-len 50 --obstacle-radius 1.0 --output-path dataset/toy_trajectories.npy
python train.py --data-path dataset/toy_trajectories.npy --checkpoint-path checkpoints/rectified_flow_mlp.pt --epochs 200 --seed 42
python recflow.py --checkpoint-path checkpoints/rectified_flow_mlp.pt --data-path dataset/toy_trajectories.npy --seed 42 --steps 20 --no-show
```

---

## 阶段二：加入 Energy-Guided 推断（`recflow_guided`）

### 要解决的问题

- Baseline 在 **OOD 障碍**（如球心移到 `(0, 1.5, 0)`）时，生成轨迹仍可能穿过障碍。
- 希望**不重训模型**，仅在采样时注入物理可行的排斥约束。

### 实现内容

- 新增 `recflow_guided.py`：与 baseline **共用同一 checkpoint**。
- 软边界球形势能：在 `r + margin` 内施加排斥梯度 `∇E`。
- 更新公式：

```text
z ← z + (v_theta(z, t) - lambda_t * grad_E(z)) * dt
```

- 可调参数：`guidance_scale`、`guidance_margin`、`guidance_decay`（constant / distance_gated）、`max_guidance_norm`。
- 新增 `evaluate.py`：固定 **ID**（障碍在原点）与 **OOD**（障碍上移）两场景，批量对比 baseline / guided。

### 实验证据（历史一次完整跑通，200 样本）

配置：`num_samples=200`, `steps=20`, `seed=42`, `scale=3`, `margin=2`, `decay=constant`。

| 场景 | 方法 | 成功率 | 碰撞率 | 平滑度↓ | 路径长度 |
|------|------|--------|--------|---------|----------|
| ID 原点 | baseline | 0.90 | 0.10 | 0.30 | 18.1 |
| ID 原点 | guided | 0.985 | 0.015 | **4.50** | **53.0** |
| OOD (0,1.5,0) | baseline | 0.855 | 0.145 | 0.30 | 18.1 |
| OOD (0,1.5,0) | guided | **1.00** | **0.00** | 0.57 | 22.4 |

（数字来源：README 记录 / 早期 `outputs/evaluation_results.json`。）

### 结论

- **OOD**：Energy Guidance 显著提升避障成功率，最小障碍距离增大，说明引导确实改变了轨迹。
- **ID**：过强 constant 引导会**过度修正**（路径变长、平滑度变差），适合作为 OOD 修补手段，不宜无条件替代 baseline。
- **答辩可强调**：同一模型、推断期加物理项、计算开销小、可解释。

### 产出物索引

- 指标：`outputs/evaluation_summary.md`、`outputs/evaluation_results.json`
- 示意图：`outputs/base_ood.png`、`outputs/guided_constant_ood.png`、`outputs/guided_distance_gated_ood.png`

---

## 阶段三：采样模块化 + 配对初始噪声（Phase 1 Step 1–2）

### 要解决的问题

1. **代码重复**：`recflow.py` 与 `recflow_guided.py` 各维护一套 Euler / 梯度 / 障碍统计。
2. **对比不够严谨**：`evaluate.py` 若依赖「两次 `set_seed`」隐式对齐噪声，难以在汇报中说明「差异只来自 guidance」。
3. **后续扩展困难**：自适应引导、随机 OOD 评测需要在多处改积分循环。

### 实现内容

| 变更 | 说明 |
|------|------|
| 新增 `flow_sampling.py` | 集中 `euler_sample`、`guided_euler_sample`、`compute_obstacle_energy_gradient`、`obstacle_distance_stats`、`load_model_from_checkpoint` 等 |
| 支持 `z_init` | `make_initial_noise(..., z_init=None)`；传入时 baseline / guided 从同一 `z0` 出发 |
| 瘦身 CLI 脚本 | `recflow.py`、`recflow_guided.py` 仅保留参数解析与可视化 |
| 更新 `evaluate.py` | 每场景生成一次 `z0`，baseline 用 `z_init`，guided 用 `z_init.clone()` |
| 文档同步 | `README.md`、`DEFENSE_NOTES.md`、`agent.md` |

### 回归验证

- `guidance_scale=0` 时，guided 与 baseline 输出一致（max diff = 0）。
- `python evaluate.py --device cpu --num-samples 50` 跑通并更新 `outputs/`。

### 实验证据（配对 z0 后，50 样本）

| 场景 | 方法 | 成功率 | 平滑度↓ | 路径长度 |
|------|------|--------|---------|----------|
| ID | baseline | 0.90 | 0.306 | 18.07 |
| ID | guided | 1.00 | 4.62 | 54.06 |
| OOD | baseline | 0.84 | 0.306 | 18.07 |
| OOD | guided | 1.00 | 0.64 | 22.94 |

**可观察现象**：两场景下 baseline 的 smoothness / path_length **完全相同**——因为 baseline 生成不依赖障碍，且两场景共用同一 `z0`；这恰好说明配对协议生效。

说明行已写入 `outputs/evaluation_summary.md`：*baseline and guided use ... initial noise z0*。

### 结论

- 工程上形成**单一采样真源**，后续 Step 3（自适应引导）可以集中修改 `flow_sampling.py`。
- 评测协议可辩护：**控制变量为 guidance 项**。
- ID 下 guided 副作用仍然存在 → 阶段四已用 **distance_gated** 进行缓解。

### 常用命令

```powershell
$env:KMP_DUPLICATE_LIB_OK='TRUE'
python evaluate.py --device cpu --num-samples 200
```

---

## 阶段四：自适应 Guidance（Phase 1 Step 3）

### 要解决的问题

- `constant` guidance 在 OOD 场景中能显著提升避障成功率，但在 ID 场景下容易过度修正，表现为路径变长、平滑度下降。
- 希望在不重新训练模型的前提下，让 guidance 更集中地作用于靠近障碍物的轨迹点，减少远离障碍区域的副作用。

### 实现内容

| 变更 | 说明 |
|------|------|
| 新增 `distance_gated` | 在 `flow_sampling.py` 中对障碍距离计算 0–1 门控，越靠近障碍排斥越强，远离障碍逐渐减弱 |
| 收窄 guidance 选项 | 移除 `linear`，当前只保留 `constant` 与 `distance_gated` 两种可解释配置 |
| 更新 CLI | `recflow_guided.py` 与 `evaluate.py` 均支持 `--guidance-decay {constant,distance_gated}` |
| 合并评估输出 | `evaluate.py` 一次运行同时输出 `baseline`、`guided_constant`、`guided_distance_gated` |
| 清理输出目录 | `outputs/` 保留统一评估结果与三张 OOD 轨迹图 |

### 回归验证

- `python -m py_compile data_generator.py model.py train.py flow_sampling.py recflow.py recflow_guided.py evaluate.py visualize_trajectories.py check_sampling_regression.py`
- `python check_sampling_regression.py --device cpu`
- `guidance_scale=0` 时，guided 与 baseline 仍完全一致（max diff = 0）。
- `python evaluate.py --device cpu` 使用现有 checkpoint 重新跑通 200 样本统一评估。

### 实验证据（200 样本）

| 场景 | 方法 | 成功率 | 碰撞率 | 最小距离 | 平滑度↓ | 路径长度↓ |
|------|------|------:|------:|------:|------:|------:|
| ID 原点 | baseline | 0.9000 | 0.1000 | 0.1206 | 0.3040 | 18.1034 |
| ID 原点 | guided_constant | 0.9850 | 0.0150 | 0.6177 | 4.4957 | 53.0077 |
| ID 原点 | guided_distance_gated | **0.9950** | **0.0050** | **0.7542** | 2.0130 | 36.9326 |
| OOD (0,1.5,0) | baseline | 0.8550 | 0.1450 | 0.1298 | 0.3040 | 18.1034 |
| OOD (0,1.5,0) | guided_constant | **1.0000** | **0.0000** | **1.4554** | 0.5742 | 22.3743 |
| OOD (0,1.5,0) | guided_distance_gated | 0.9950 | 0.0050 | 0.9945 | **0.4701** | **20.5781** |

### 结论

- `distance_gated` 在 OOD 场景下仍显著优于 baseline，同时比 `constant` guidance 更平滑、路径更短。
- 在 ID 场景中，`distance_gated` 保持高成功率，并明显缓解 `constant` guidance 的过度修正问题。
- 当前输出统一为：
  - `outputs/evaluation_results.json`
  - `outputs/evaluation_summary.md`
  - `outputs/base_ood.png`
  - `outputs/guided_constant_ood.png`
  - `outputs/guided_distance_gated_ood.png`

### 常用命令

```powershell
$env:KMP_DUPLICATE_LIB_OK='TRUE'
python evaluate.py --device cpu
python recflow.py --checkpoint-path checkpoints/rectified_flow_mlp.pt --data-path dataset/toy_trajectories.npy --seed 42 --steps 20 --num-samples 50 --obstacle-center 0 1.5 0 --obstacle-radius 1.0 --save-fig outputs/base_ood.png --no-show
python recflow_guided.py --checkpoint-path checkpoints/rectified_flow_mlp.pt --data-path dataset/toy_trajectories.npy --seed 42 --steps 20 --num-samples 50 --obstacle-center 0 1.5 0 --obstacle-radius 1.0 --guidance-scale 3.0 --guidance-margin 2.0 --guidance-decay constant --max-guidance-norm 10.0 --save-fig outputs/guided_constant_ood.png --no-show
python recflow_guided.py --checkpoint-path checkpoints/rectified_flow_mlp.pt --data-path dataset/toy_trajectories.npy --seed 42 --steps 20 --num-samples 50 --obstacle-center 0 1.5 0 --obstacle-radius 1.0 --guidance-scale 3.0 --guidance-margin 2.0 --guidance-decay distance_gated --max-guidance-norm 10.0 --save-fig outputs/guided_distance_gated_ood.png --no-show
```

---

## 阶段五：多障碍扩展（Phase 1 Step 4）

### 要解决的问题

- 单球障碍只能验证最简单的避障泛化，不能说明 guidance 是否可以扩展到多个障碍物。
- 后续随机 OOD 和更复杂场景需要统一的多障碍梯度叠加与碰撞统计接口。

### 实现内容

| 变更 | 说明 |
|------|------|
| 多障碍梯度 | `flow_sampling.py` 支持多个球形障碍物的能量梯度叠加 |
| 多障碍门控 | `distance_gated` 对多个障碍取最大距离门控，靠近任一障碍时增强排斥 |
| 多障碍统计 | `obstacle_distance_stats` 支持 `(M, 3)` 障碍中心与 `(M,)` 半径；任一障碍碰撞即失败 |
| Guided CLI | `recflow_guided.py` 新增可重复的 `--obstacle X Y Z R`，并兼容旧的 `--obstacle-center/--obstacle-radius` |
| 双障碍评估 | `evaluate.py` 默认加入 `ood_double_gap` 场景，同时评估 baseline、constant、distance_gated |

### 实验证据（200 样本）

| 场景 | 方法 | 成功率 | 碰撞率 | 最小距离 | 平滑度↓ | 路径长度↓ |
|------|------|------:|------:|------:|------:|------:|
| OOD 双障碍 | baseline | 0.6150 | 0.3850 | 0.0978 | 0.3040 | 18.1034 |
| OOD 双障碍 | guided_constant | **0.9700** | **0.0300** | **0.8078** | 4.7778 | 52.0974 |
| OOD 双障碍 | guided_distance_gated | 0.9300 | 0.0700 | 0.6662 | **1.8873** | **34.2087** |

### 结论

- 多障碍势能叠加在双球夹缝场景中显著提升成功率，说明推断期 guidance 可以从单障碍自然扩展到多障碍。
- `guided_constant` 成功率最高，但路径和平滑度代价更大；`guided_distance_gated` 成功率仍远高于 baseline，同时路径更短、更平滑。
- 新增示意图：`outputs/guided_distance_gated_double_ood.png`。
- 双障碍图组：
  - `outputs/base_double_ood.png`
  - `outputs/guided_constant_double_ood.png`
  - `outputs/guided_distance_gated_double_ood.png`

### 常用命令

```powershell
$env:KMP_DUPLICATE_LIB_OK='TRUE'
python evaluate.py --device cpu
python recflow.py --checkpoint-path checkpoints/rectified_flow_mlp.pt --data-path dataset/toy_trajectories.npy --seed 42 --steps 20 --num-samples 50 --obstacle 0 1.5 0 1.0 --obstacle 0 -1.5 0 1.0 --save-fig outputs/base_double_ood.png --no-show
python recflow_guided.py --checkpoint-path checkpoints/rectified_flow_mlp.pt --data-path dataset/toy_trajectories.npy --seed 42 --steps 20 --num-samples 50 --obstacle 0 1.5 0 1.0 --obstacle 0 -1.5 0 1.0 --guidance-scale 3.0 --guidance-margin 2.0 --guidance-decay constant --max-guidance-norm 10.0 --save-fig outputs/guided_constant_double_ood.png --no-show
python recflow_guided.py --checkpoint-path checkpoints/rectified_flow_mlp.pt --data-path dataset/toy_trajectories.npy --seed 42 --steps 20 --num-samples 50 --obstacle 0 1.5 0 1.0 --obstacle 0 -1.5 0 1.0 --guidance-scale 3.0 --guidance-margin 2.0 --guidance-decay distance_gated --max-guidance-norm 10.0 --save-fig outputs/guided_distance_gated_double_ood.png --no-show
```

---

## 阶段六：随机 OOD 评估（Phase 1 Step 5/6）

### 要解决的问题

- 固定 OOD 点和双障碍 demo 仍然是少量手工场景，不能充分说明方法对不同障碍位置的稳定性。
- 需要用随机障碍分布评估 baseline、`guided_constant` 与 `guided_distance_gated` 的平均表现。

### 实现内容

| 变更 | 说明 |
|------|------|
| 随机场景生成 | `evaluate.py` 新增 `--random-ood-count N`，追加 N 个随机单障碍 OOD 场景 |
| 可控采样范围 | 支持 `--random-ood-y-range`、`--random-ood-z-range`、`--random-ood-radius-range` |
| 排除近原点样本 | `--random-ood-min-center-norm` 避免随机障碍过于接近训练内原点障碍 |
| 汇总输出 | Markdown 与 JSON 中加入 `random_ood_summary`，统计随机场景均值 |

### 实验证据（20 个随机 OOD 场景，200 样本）

采样配置：`y ∈ [-2.5, 2.5]`，`z ∈ [-1.5, 1.5]`，`radius ∈ [0.8, 1.2]`，`min_center_norm = 1.0`。

| 方法 | 成功率 | 碰撞率 | 最小距离 | 平滑度↓ | 路径长度↓ |
|------|------:|------:|------:|------:|------:|
| baseline | 0.8732 | 0.1267 | 0.1680 | 0.3040 | 18.1034 |
| guided_constant | **0.9995** | **0.0005** | **1.6380** | 0.6269 | 22.4427 |
| guided_distance_gated | 0.9975 | 0.0025 | 1.1977 | **0.4895** | **20.6685** |

### 结论

- 随机 OOD 结果说明 Energy Guidance 的提升不是只对固定 `(0, 1.5, 0)` 场景有效。
- `guided_constant` 仍给出最高成功率和最小碰撞率；`guided_distance_gated` 成功率非常接近，同时保持更低平滑度代价和更短路径。
- 主结果已合并到 `outputs/evaluation_results.json` 与 `outputs/evaluation_summary.md`。

### 常用命令

```powershell
python evaluate.py --device cpu --random-ood-count 20
```

---

## 阶段七：Guidance 参数消融（Phase 1 Step 7）

### 要解决的问题

- 主实验采用 `scale=3.0, margin=2.0, max_norm=10.0`，需要说明这些参数对成功率、路径长度和平滑度的影响。
- `constant` 与 `distance_gated` 的取舍需要更系统的证据，而不只是单点实验。

### 实现内容

| 变更 | 说明 |
|------|------|
| 新增消融脚本 | `ablate_guidance.py` 支持 `guidance_scale`、`guidance_margin`、`max_guidance_norm` 三组 sweep |
| 统一评估协议 | 每组消融覆盖 ID 原点、`ood_shifted_y`、`ood_double_gap`，并复用配对 `z0` 思路 |
| 自动产物 | 输出 Markdown summary、JSON results、Pareto CSV 与折线图 |
| 输出位置 | `outputs/ablation_guidance_summary_*.md`、`outputs/ablation_guidance_pareto_*.csv`、`outputs/ablation_plots/*.png` |

### 实验证据（每个配置 500 样本）

关键观察：

| 消融项 | 现象 | 可讲结论 |
|------|------|------|
| `guidance_scale` | OOD 成功率随 scale 增大快速提升；ID / 双障碍中的路径长度和平滑度代价也同步增大 | scale 是主要 trade-off 旋钮，默认 `3.0` 偏向安全 |
| `guidance_margin` | margin 从 `0` 增至 `1.5~2.0` 明显改善 OOD；继续增大在双障碍中会造成路径急剧变长 | margin 控制“提前避障”的范围，过大容易过度绕行 |
| `max_guidance_norm` | OOD 单障碍在较小 norm 下已接近满成功；双障碍需要更大 norm，但收益在 `6~8` 后趋于饱和 | norm 裁剪限制极端引导，避免无界梯度导致轨迹质量崩坏 |

代表性数字：

- `guidance_scale` sweep 中，`ood_shifted_y` baseline 成功率 `0.7620`；`constant scale=2.0` 已达 `1.0000`，`distance_gated scale=3.0` 达 `0.9980` 且路径更短。
- `guidance_margin` sweep 中，`ood_double_gap` baseline 成功率 `0.5580`；`constant margin=1.5` 达 `0.9480`，`distance_gated margin=2.0` 达 `0.9480` 且平滑度代价更低。
- `max_guidance_norm` sweep 中，`ood_double_gap` 的 `constant` 在 norm `6.0` 后稳定在 `0.9620` 左右，`distance_gated` 在 norm `5.0~6.0` 达到 `0.9420~0.9520`，路径明显短于 constant。

### 结论

- 消融验证了 guidance 的核心 trade-off：更强引导通常带来更高成功率和更大安全距离，但也会拉长路径、降低平滑性。
- `distance_gated` 不是单纯追求最高成功率，而是在成功率接近 `constant` 的情况下明显降低轨迹质量代价，因此适合作为答辩中的推荐默认方法。
- 产物已经可直接用于 README、汇报图和答辩备份材料。

### 常用命令

```powershell
python ablate_guidance.py --device cpu --ablate guidance_scale --num-samples 500
python ablate_guidance.py --device cpu --ablate guidance_margin --num-samples 500
python ablate_guidance.py --device cpu --ablate max_guidance_norm --num-samples 500
```

---

## 阶段八：Conditional Rectified Flow（Phase 2）

### 要解决的问题

- Phase 1 的 Energy Guidance 是推断期启发式修正，模型本身仍不显式理解障碍物参数。
- 希望把障碍物位置和半径作为训练条件输入，让速度场学习 `v_theta(x_t, t, c)`，观察是否能减少对推断期 guidance 的依赖。

### 实现内容

| 变更 | 说明 |
|------|------|
| 条件数据集 | `generate_conditional_data.py` 生成 `.npz`，保存 `trajectories`、`conditions`、`obstacle_centers`、`obstacle_radii` |
| 条件表示 | 每个障碍物编码为 `(cx, cy, cz, radius)`；默认 `max_obstacles=2`，所以 `conditions` 形状为 `(N, 8)` |
| 条件模型 | `RectifiedFlowConditionalMLP` 在轨迹状态和时间嵌入之外拼接 condition |
| 条件训练 | `train_conditional.py` 使用同一 Rectified Flow 目标：`MSE(v_theta(x_t,t,c), x1-x0)` |
| 四路评测 | `evaluate.py --conditional-checkpoint-path ...` 输出 `baseline`、`guided_*`、`conditional`、`conditional_guided_*` |
| 可视化 | `recflow_conditional.py` 支持 conditional 与 conditional+guided 轨迹图 |
| Conditional 消融 | `ablate_guidance.py --conditional-checkpoint-path ...` 复用 guidance sweep；图中对比 `constant`、`distance_gated`、`cond_constant`、`cond_distance_gated` 四条曲线 |

### 实验证据（200 样本，distance_gated）

配置：`num_samples=200`, `steps=20`, `seed=42`, `scale=3`, `margin=2`, `max_norm=10`。

| 场景 | 方法 | 成功率 | 碰撞率 | 最小距离 | 平滑度↓ | 路径长度↓ |
|------|------|------:|------:|------:|------:|------:|
| ID 原点 | baseline | 0.7500 | 0.2500 | 0.0847 | 0.2620 | 17.2844 |
| ID 原点 | guided_distance_gated | 0.9800 | 0.0200 | 0.6033 | 2.3036 | 38.8434 |
| ID 原点 | conditional | 0.7450 | 0.2550 | 0.0795 | 0.2865 | 17.7527 |
| ID 原点 | conditional_guided_distance_gated | 0.9750 | 0.0250 | 0.8475 | 2.6151 | 41.3636 |
| OOD (0,1.5,0) | baseline | 0.7800 | 0.2200 | 0.1062 | 0.2620 | 17.2844 |
| OOD (0,1.5,0) | guided_distance_gated | **1.0000** | **0.0000** | 1.0205 | **0.4709** | **20.2886** |
| OOD (0,1.5,0) | conditional | 0.8150 | 0.1850 | 0.1949 | 0.2845 | 17.7240 |
| OOD (0,1.5,0) | conditional_guided_distance_gated | **1.0000** | **0.0000** | **1.3255** | 0.4865 | 20.6979 |
| OOD 双障碍 | baseline | 0.5750 | 0.4250 | 0.0609 | 0.2620 | 17.2844 |
| OOD 双障碍 | guided_distance_gated | 0.9550 | 0.0450 | **0.7946** | 1.9563 | 34.8642 |
| OOD 双障碍 | conditional | 0.7200 | 0.2800 | 0.2038 | **0.2893** | **17.8497** |
| OOD 双障碍 | conditional_guided_distance_gated | **0.9700** | **0.0300** | 0.5774 | 1.9517 | 35.2166 |

### 结论

- 纯 `conditional` 在 OOD 单障碍与双障碍场景中均优于 uncond baseline，说明障碍条件输入提供了有效信息。
- 纯 `conditional` 尚未替代推断期 guidance；它保持更短路径和更低平滑度代价，但成功率提升有限。
- `conditional_guided_distance_gated` 在 OOD 单障碍达到 `1.0000` 成功率，并在双障碍中达到 `0.9700`，是当前四路中最稳的组合。
- 可视化输出：
  - `outputs/conditional_ood.png`
  - `outputs/conditional_guided_ood.png`
  - `outputs/evaluation_conditional_summary.md`
  - `outputs/evaluation_conditional_results.json`

### 常用命令

```powershell
python generate_conditional_data.py --num-trajectories 5000 --seq-len 50 --max-obstacles 2 --min-obstacles 1 --max-active-obstacles 2 --output-path dataset/conditional_trajectories.npz
python train_conditional.py --data-path dataset/conditional_trajectories.npz --checkpoint-path checkpoints/rectified_flow_conditional_mlp.pt --epochs 200 --seed 42
python evaluate.py --device cpu --conditional-checkpoint-path checkpoints/rectified_flow_conditional_mlp.pt --guidance-decay distance_gated --output-json outputs/evaluation_conditional_results.json --output-markdown outputs/evaluation_conditional_summary.md
python recflow_conditional.py --device cpu --num-samples 50 --steps 20 --obstacle-center 0 1.5 0 --obstacle-radius 1.0 --save-fig outputs/conditional_ood.png --save-generated outputs/conditional_ood.npy --no-show
python recflow_conditional.py --device cpu --num-samples 50 --steps 20 --obstacle-center 0 1.5 0 --obstacle-radius 1.0 --guided --save-fig outputs/conditional_guided_ood.png --save-generated outputs/conditional_guided_ood.npy --no-show
python ablate_guidance.py --device cpu --conditional-checkpoint-path checkpoints/rectified_flow_conditional_mlp.pt --ablate guidance_scale --num-samples 500 --output-json outputs/ablation_conditional_guidance_results.json --output-markdown outputs/ablation_conditional_guidance_summary.md --output-csv outputs/ablation_conditional_guidance_pareto.csv --plot
```

---

## 当前仓库结构（推断相关）

```text
flow_sampling.py    # 采样、多障碍能量梯度与 distance_gated 自适应引导
recflow.py          # Baseline CLI 与 OOD 图生成
recflow_guided.py   # Guided CLI，支持 constant / distance_gated 与多障碍输入
recflow_conditional.py # Conditional / Conditional+Guided CLI 与 OOD 图生成
evaluate.py         # 批量评测（配对 z0，统一输出三方法、多障碍和随机 OOD 对比）
ablate_guidance.py  # guidance 参数消融、Pareto CSV 与可视化图
train.py            # Unconditional 训练
train_conditional.py # Conditional 训练
```

---

## 汇报时可用的三条主线

1. **我们复现了什么**：Rectified Flow 在 3D 轨迹上的完整 pipeline（阶段一）。
2. **我们的创新点是什么**：推断期 Energy Guidance，OOD 避障显著提升（阶段二）。
3. **我们如何保证对比可信**：模块化采样 + 配对 `z0`（阶段三）；多障碍、随机 OOD、参数消融和 conditional 四路对比共同支撑结论。

---

## 已知局限（主动说明）

| 局限 | 说明 |
|------|------|
| 障碍几何 | 支持静态单球 / 多球软边界；尚未支持复杂几何或动态障碍 |
| Guidance | 不参与 unconditional 训练；constant 引导在 ID 下路径过长，`distance_gated` 只能缓解 trade-off |
| 模型容量 | 整段 MLP，非序列 Transformer |
| Conditional | 条件输入仍是球形障碍参数，尚未引入 SDF / occupancy 等复杂环境表示 |
| 评测规模 | 已有固定 / 双障碍 / 随机 OOD、消融与 conditional 四路对比；仍不是大规模规划 benchmark |
| 复现资产 | `dataset/`、`checkpoints/` 在 `.gitignore`，克隆后需本地生成 |

---

## 待办（按优先级）

### Phase 1（推断期方法深化）

- [x] **Step 3**：`distance_gated` 自适应引导
- [x] **Step 4**：多障碍物势能叠加 + 双球夹缝 demo
- [x] **Step 5/6**：固定 OOD + `evaluate.py --random-ood-count` 随机障碍分布评测
- [x] **Step 7**：`ablate_guidance.py` + Pareto CSV / 图；README 主表与当前 200 样本结果对齐

### Phase 2（训练期创新）

- [x] 条件数据生成脚本：`generate_conditional_data.py`，保存轨迹、障碍参数与展平 condition
- [x] `RectifiedFlowConditionalMLP` + `train_conditional.py`
- [x] `evaluate.py` 支持四路对比：uncond / uncond+guided / cond / cond+guided
- [x] `recflow_conditional.py` 支持 conditional / conditional+guided 可视化
- [x] 跑完 conditional 训练与正式四路评测，补充结果表
- [x] `ablate_guidance.py` 支持 conditional guidance ablation 接口
- [ ] 进一步调参或扩展到 SDF / occupancy 条件表示

---

## 文档与计划索引

| 文档 | 用途 |
|------|------|
| [README.md](README.md) | 安装、命令、方法简介 |
| [DEFENSE_NOTES.md](DEFENSE_NOTES.md) | 答辩讲述顺序 |
| [agent.md](agent.md) | 开发规范与数学定义 |
| 本文档 `PROJECT_PROGRESS.md` | **阶段工作与证据链** |
| `.cursor/plans/phase1-step-by-step_*.plan.md` | 开发待办（本地） |
| `.cursor/plans/substantive-innovation-roadmap_*.plan.md` | 中长期路线（本地） |

---

## 更新记录

| 日期 | 摘要 |
|------|------|
| 2026-05 | 阶段一：Baseline 框架与训练推断闭环 |
| 2026-05 | 阶段二：`recflow_guided` + `evaluate.py` + OOD 对比实验 |
| 2026-05 | 阶段三：`flow_sampling.py`、配对 `z0`、文档同步 |
| 2026-05 | 阶段四：`distance_gated` 自适应引导、三方法统一评估、OOD 轨迹图更新 |
| 2026-05 | 阶段五：多障碍势能叠加、`ood_double_gap` 评估、双障碍轨迹图 |
| 2026-05 | 阶段六：随机 OOD 场景评估与均值汇总 |
| 2026-06 | 阶段七：guidance 参数消融、Pareto CSV / 图与文档同步 |
| 2026-06 | Phase 2：conditional 数据、模型、训练脚本、可视化、四路评测与 conditional ablation 接口 |

*后续扩展 SDF 条件输入、序列模型或新增 benchmark 时，请继续追加「实现 / 证据 / 结论」，并更新本表。*
