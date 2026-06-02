# Work Log

> 项目开发日志 — 记录关键里程碑、设计决策和教训。完整命令见 [CLAUDE.md](CLAUDE.md)，实验结果见 [README.md](README.md)。

## Milestones

| 日期 | 阶段 | 交付 | 关键决策 |
|------|------|------|----------|
| 2026-05 | Baseline | `data_generator` → `train` → `recflow` 闭环 | MLP + 正弦时间嵌入，Bezier 专家轨迹 |
| 2026-05 | Energy Guidance | `recflow_guided` + `evaluate.py` | 推断期球形软边界排斥势能，不重训模型 |
| 2026-05 | 采样模块化 | `flow_sampling.py` 统一四种采样函数 | 配对 `z0` 公平评测（baseline/guided 从同一噪声出发） |
| 2026-05 | `distance_gated` | 距离门控引导 | 舍弃 `linear` 衰减，只留 `constant` / `distance_gated` |
| 2026-05 | 多障碍 | 梯度叠加 + 门控取 max | `--obstacle X Y Z R` 可重复传入 |
| 2026-05 | 随机 OOD | `evaluate.py --random-ood-count N` | 均值汇总证明 guidance 不是只对单个场景有效 |
| 2026-06 | 消融 | `ablate_guidance.py` | scale/margin/norm 三参数 sweep，500 样本 |
| 2026-06 | Conditional RF | `RectifiedFlowConditionalMLP` + 四路评测 | 障碍参数展平 `[cx,cy,cz,r,...]×2` 作为条件输入 |
| 2026-06 | Conditional 消融 | 四曲线对比 | 条件模型 + guidance 存在互补效应 |

## Design Decisions

### 为什么用 Rectified Flow 而非 DDPM
- Euler 积分步数少（20 步即可），轨迹是直线插值路径，训练更稳定。

### 为什么 `distance_gated` 而非更复杂的自适应
- 尝试过 `risk_adaptive`（三因子：距离 × 时间 × 风险门控），但时间门控在任何 p>0 时都会伤害成功率（早期引导对轨迹形状至关重要），风险门控只比 `distance_gated` 多节省 ~13% 平滑度，性价比低。**已废弃。**
- `distance_gated` 足够简单有效：成功率接近 `constant`，平滑度降低 50-60%，路径缩短 30-35%。

### 为什么条件编码用拼接而非交叉注意力
- 条件维度仅 8（2 个障碍物 × 4 参数），拼接到 150 维轨迹输入中足够区分。对于这种小规模参数空间，简单拼接优于复杂机制。

### 为什么保留配对 z0 评测
- 同一场景下 baseline 和 guided 从同一初始噪声出发，差异唯一来自 guidance 项。若分别随机初始化，方差会混淆方法效果。

## Dead Ends

| 尝试 | 结果 | 教训 |
|------|------|------|
| `risk_adaptive`（距离+时间+风险三门控） | `time_decay_power` 必须为 0（时间门控反效果）；`risk_quantile` 最优值 0.5，相比 `distance_gated` 仅省 13% 平滑度 | 三门控叠加过度稀释有效引导强度；时间衰减在 Rectified Flow 中不适用（早期步对轨迹形状更关键） |
| `linear` 衰减模式 | 线性过渡不如硬阈值+平滑衰减直观 | 被 `distance_gated` 替代 |

## Current Status

- **Unconditional pipeline**: 完整（数据 → 训练 → 两种 guidance → 多障碍 → 随机 OOD → 消融）
- **Conditional pipeline**: 完整（数据 → 训练 → 条件采样 → 条件引导 → 四路评测 → 条件消融）
- **最佳方法**: `conditional + distance_gated`，双障碍成功率 0.970
- **推荐参数**: `scale=3.0, margin=2.0, max_norm=10.0, decay=distance_gated`

## Next

- [ ] Classifier-Free Guidance：让条件模型在推断时内化避障行为，减少对物理启发式引导的依赖
- [ ] 答辩图表整理
