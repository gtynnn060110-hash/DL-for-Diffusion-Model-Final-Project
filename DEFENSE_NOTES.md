# 答辩叙事提纲

## 一句话项目定位

本项目复现 Rectified Flow 在 3D 轨迹生成上的基础流程，并沿两条互补路线提升 OOD 避障能力：**推断期 Energy Guidance**（不重训模型，物理启发式排斥）与 **训练期 Conditional Rectified Flow**（障碍参数作为条件输入）。两条路线可叠加，conditional + distance_gated 是当前最强组合。

## 推荐讲述顺序

1. **问题背景**
   - 生成模型不只适用于图像，也可以生成连续空间中的运动轨迹。
   - 轨迹生成需要同时考虑生成质量、采样速度和物理约束。
   - 标准扩散模型通常需要较多采样步数，面对新的障碍物设置时也缺少直接适应能力。

2. **Baseline 复现**
   - `data_generator.py` 生成 3D Bezier 专家轨迹（起点 (-5,0,0)，终点 (5,0,0)，绕开原点障碍）。
   - `train.py` 训练 Rectified Flow 速度场：`MSE(v_θ(x_t, t), x1 - x0)`。
   - `recflow.py` 从高斯噪声用 Euler 积分采样完整轨迹。
   - 价值：证明模型可以学习平滑轨迹分布；但 baseline 不感知推断时的障碍物位置。

3. **Baseline 的局限 → Energy Guidance**
   - Baseline 只学训练分布，OOD 障碍下可能穿障。
   - 方案：推断期不重训，在 Euler 步中注入障碍物排斥势能梯度。
   - 更新公式：`z ← z + (v_θ - λ·∇E) · dt`
   - 两种模式：`constant`（全程强引导）和 `distance_gated`（仅在靠近障碍时激活，减少远距离扰动）。
   - 核心优势：无需重训、解释性强、计算开销小。

4. **从单障碍到系统化评测**
   - 采样模块化（`flow_sampling.py` 统一四种采样函数）。
   - 配对 z0 公平评测：baseline 和 guided 从同一初始噪声出发，差异仅来自 guidance。
   - 多障碍支持（梯度叠加 + 门控取 max）→ 双球夹缝场景。
   - 随机 OOD 评估（20 个随机障碍场景，均值汇总）→ 证明不是只对单个场景有效。
   - 参数消融（scale / margin / max_norm × 500 样本 × 3 场景）→ 系统刻画 trade-off。

5. **Conditional Rectified Flow（Phase 2）**
   - 思路：不只靠推断期修补，让模型在训练时就显式感知障碍物参数。
   - 条件编码：障碍物展平为 `[cx1, cy1, cz1, r1, cx2, cy2, cz2, r2]`（`max_obstacles=2`），拼接到模型输入。
   - `RectifiedFlowConditionalMLP` 学习 `v_θ(x, t, c)`。
   - 四路对比：baseline / guided / conditional / conditional+guided。
   - 条件消融：四曲线对比（constant / dg / cond_const / cond_dg）。

## 建议展示图表

- 专家轨迹 vs Baseline 生成轨迹对比图
- OOD 障碍下 Guided 对比图（单障碍 + 双障碍）
- 四路对比指标表（`outputs/evaluation_conditional_summary.md`）
- 消融曲线（`outputs/ablation_plots/`），重点展示 distance_gated 如何在接近 constant 成功率的同时大幅降低平滑度代价
- Conditional 可视化图：`outputs/conditional_ood.png` / `outputs/conditional_guided_ood.png`

## 关键数字

无条件模型（200 样本，scale=3, margin=2）：
- `ood_shifted_y`：baseline 0.855 → guided 1.000
- `ood_double_gap`：baseline 0.615 → guided 0.970
- `distance_gated` 平滑度比 `constant` 低 50-60%，路径短 30-35%

条件模型四路对比（200 样本，distance_gated）：
- `ood_shifted_y`：baseline 0.780 → conditional 0.815 → guided 1.000 → cond+guided 1.000
- `ood_double_gap`：baseline 0.575 → conditional 0.720 → guided 0.955 → cond+guided 0.970
- 纯 conditional 在双障碍优于 baseline +14.5%，说明模型从条件中学习了避障
- cond+guided 是当前最强组合

消融发现（500 样本）：
- 条件模型可在略低 guidance 强度下达到同等成功率，印证训练期条件与推断期引导的互补
- `distance_gated` 允许用更高 scale 换取成功率，而不像 `constant` 那样平滑度/路径代价暴涨

## 需要主动说明的局限

- 障碍物建模为静态球形软边界，尚未覆盖复杂几何或动态障碍。
- Energy guidance 是推断期启发式方法，不是训练得到的全局规划器；强引导会带来轨迹扭曲。
- 当前模型是整段轨迹 MLP（非序列 Transformer）。
- Conditional 使用简单拼接条件；下一步计划探索 Classifier-Free Guidance 等更强条件机制。

## 结论表达

当前项目形成"无条件管道 → Energy Guidance（constant / distance_gated）→ Conditional RF → 四路对比 → 双线消融"的完整闭环。核心论点：

1. Rectified Flow 能用较少步数从噪声生成平滑 3D 轨迹。
2. Energy Guidance 在**不重训模型**的前提下，将 OOD 避障成功率从 0.62-0.86 提升到 0.97-1.00；`distance_gated` 在大幅保持成功率的同时显著降低轨迹质量代价。
3. Conditional RF 将障碍参数纳入模型训练，纯条件已在 OOD 场景超越无条件 baseline，与 guidance 叠加后达到最强性能。
4. 两条路线互补——条件模型内化避障知识，推断期 guidance 提供精确物理约束。
