# 答辩叙事提纲

## 一句话项目定位

本项目复现 Rectified Flow 在 3D 轨迹生成上的基础流程，并在不重新训练模型的前提下，引入推断期能量引导来提升障碍物场景下的避障成功率。

## 推荐讲述顺序

1. **问题背景**
   - 生成模型不只适用于图像，也可以生成连续空间中的运动轨迹。
   - 轨迹生成需要同时考虑生成质量、采样速度和物理约束。
   - 标准扩散模型通常需要较多采样步数，面对新的障碍物设置时也缺少直接适应能力。

2. **Baseline 复现**
   - 使用 `data_generator.py` 生成三维专家轨迹。
   - 使用 `train.py` 训练 Rectified Flow 速度场模型。
   - 使用 `recflow.py` 从高斯噪声采样生成完整轨迹。
   - Baseline 的价值是证明模型可以学习平滑轨迹分布。

3. **Baseline 的局限**
   - 模型只学习训练数据分布，不显式感知推断时的障碍物设置。
   - 当障碍物位置或半径变为 OOD 设置时，baseline 可能生成穿过障碍物的轨迹。

4. **Energy Guidance 改进**
   - `recflow_guided.py` 使用同一个 checkpoint。
   - 在 Euler 采样阶段加入球形障碍物的软排斥势能梯度。
   - 更新公式从 `x = x + v * dt` 变为 `x = x + (v - guidance) * dt`。
   - 核心优势是无需重训、解释性强、计算开销小。

5. **实验验证**
   - `evaluate.py` 统一比较 baseline 和 guided。
   - 主要指标：`success_rate`、`collision_rate`、`min_distance_to_obstacle`、`smoothness`、推理耗时。
   - 最重要的对比是 OOD 障碍物场景，因为它更能体现推断期 guidance 的价值。

## 建议展示图表

- 数据生成得到的专家轨迹图。
- Baseline 生成轨迹和真实轨迹对比图。
- Guided 生成轨迹在 OOD 障碍物下的对比图。
- `evaluate.py` 输出的指标表，重点突出 success rate 和 min distance。

## 需要主动说明的局限

- 当前障碍物只建模为球形软边界。
- Guidance 是推断期启发式方法，不是训练得到的全局规划器。
- 当前模型是整段轨迹 MLP，不处理更复杂的动态环境。
- 后续可扩展为条件 Flow Matching，将障碍物参数或 SDF 作为模型输入。

## 结论表达

当前项目已经形成“数据生成 -> 训练 -> baseline 推断 -> energy-guided 推断 -> 批量评测”的完整闭环。实验重点应放在证明：在同一个模型 checkpoint 下，推断期能量引导可以以较小计算代价改善 OOD 障碍物设置下的避障表现。
