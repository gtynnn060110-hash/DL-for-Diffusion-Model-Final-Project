# Rectified Flow 基础复现项目

## 1. 项目目标
复现论文 *Flow Straight and Fast: Learning to Generate and Edit Data with Rectified Flow* 的核心算法（1-Rectified Flow）。
构建一个能够将高斯噪声 $X_0$ 映射到 3D 避障轨迹 $X_1$ 的生成模型。

## 2. 核心数学逻辑 (核心指令)
Agent 在编写代码时必须严格遵守以下数学定义：

* **线性插值 (训练目标 $X_t$):** $X_t = t X_1 + (1 - t) X_0$, 其中 $t \sim \text{Uniform}([0, 1])$
* **训练损失函数 (Loss):** $\mathcal{L} = \text{MSE}\left( v_\theta(X_t, t), X_1 - X_0 \right)$
* **推理/采样公式 (ODE 求解 $Z$):** $Z_{t+\Delta t} = Z_t + v_\theta(Z_t, t) \cdot \Delta t$ (使用 Euler 方法)

## 3. 任务分解 (Phase Breakdown)

### Phase 1: 数据生成器 (`data_generator.py`)
* **目标**: 生成专家轨迹 $X_1$。
* **逻辑**: 使用 3D 贝塞尔曲线。固定起点 $[-5, 0, 0]$ 和终点 $[5, 0, 0]$，障碍物在 $[0, 0, 0]$。随机化控制点以确保轨迹多样性（例如让曲线向上或向两侧凸起绕过原点）。
* **输出**: 形状为 `(N, 50, 3)` 的 NumPy 数组或 PyTorch Tensor（N=5000）。保存为本地文件。

### Phase 2: 模型定义 (`model.py`)
* **架构**: 一个轻量级的多层感知机 (MLP) 或 1D-Transformer。
* **输入**: 
    * `x`: 轨迹状态，形状为 `(Batch, 150)` (将 50x3 拉平) 或 `(Batch, 50, 3)`。
    * `t`: 标量时间，形状为 `(Batch, 1)`。必须使用正弦位置编码 (Sinusoidal Positional Embedding) 或直接与 `x` 拼接。
* **输出**: 与输入 `x` 形状完全相同的速度向量场。

### Phase 3: 训练脚本 (`train.py`)
* **核心步骤**:
    1.  加载 Phase 1 生成的 $X_1$ 轨迹数据，构建 DataLoader。
    2.  在每个 iteration 中，生成与 $X_1$ 同形状的标准高斯噪声 $X_0 \sim \mathcal{N}(0, I)$。
    3.  随机采样时间 $t \sim U(0, 1)$。
    4.  按公式计算插值点 $X_t$。
    5.  计算模型预测速度 $v_\theta(X_t, t)$ 与目标速度 $(X_1 - X_0)$ 的 MSE 损失。
    6.  使用 AdamW 优化器反向传播更新参数。

### Phase 4: 推理与可视化 (`recflow.py`)
* **核心步骤**:
    1.  初始化纯高斯噪声 $Z_0$。
    2.  实现欧拉积分器（Euler Method），设定步数（例如 10 步）。
    3.  在每一步中，计算 $Z_{t+\Delta t} = Z_t + v_\theta(Z_t, t) \cdot \Delta t$。
    4.  使用 `matplotlib` 或 `plotly` 将生成的轨迹 $Z_1$ 与训练集中的真实轨迹 $X_1$ 进行 3D 可视化对比。

## 4. 技术规格要求
* **Framework**: `PyTorch`
* **Data Types**: `torch.float32`
* **Tensor Shapes**:
    * `X_1`: `(Batch, Sequence_Length, Dim)` -> `(Batch, 50, 3)`
    * `t`: `(Batch, 1, 1)` 或 `(Batch, 1)` 用于广播计算。
* **Device**: 优先检测 `cuda`，若无则检测 `mps` (Mac)，最后降级使用 `cpu`。代码需具备设备兼容性。
