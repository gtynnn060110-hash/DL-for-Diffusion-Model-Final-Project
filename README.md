# 大作业项目：基于能量引导流匹配的动态避障轨迹生成
**(Energy-Guided Flow Matching for Dynamic Obstacle Avoidance)**

## 1. 选题背景与 AIGC 领域契合度
本项目聚焦于 AIGC 领域的**世界模型（World Models）与生成式具身智能**方向。
目前主流的生成模型多关注于离散像素（图像/视频），而探索连续物理空间中的运动学轨迹生成，是生成模型走向物理世界的前沿关键。传统的扩散模型（Diffusion）在轨迹生成中存在采样步数多、推理慢的问题，且面对训练分布外（OOD）的新障碍物时缺乏零样本适应能力。本项目旨在通过流匹配（Flow Matching）与能量引导（Energy Guidance）解决这一瓶颈。

## 2. 经典工作复现 (Baseline)
本项目的基础底座将严格复现以下经典生成模型理论：
*   **核心理论**：*Flow Matching for Generative Modeling* (Lipman et al., 2023) 与 *Rectified Flow* (Liu et al., 2022)。
*   **实现目标**：构建并训练一个基于 MLP 或 1D-DiT 架构的常微分方程（ODE）速度场预测网络 $v_\theta(x_t, t)$。实现从高斯噪声 $X_0 \sim \mathcal{N}(0, I)$ 到平滑无障碍物理轨迹 $X_1$ 的极速生成（$\le 10$ 步）。

## 3. 创新改进与核心技术路线
### 3.1 核心痛点
基础流匹配模型仅能生成拟合训练数据分布的轨迹。在推理阶段若环境中随机出现动态障碍物，原生模型生成的轨迹极易发生“穿模”或碰撞。

### 3.2 我们的创新：能量引导推理 (Energy-Guided Inference)
借鉴扩散模型中的分类器引导（Classifier-Guidance）思想，我们在**不重新训练基础流匹配网络**的前提下，在 ODE 推理阶段引入物理排斥势能场。当前实现中，`recflow.py` 和 `recflow_guided.py` 使用**同一个训练好的 Rectified Flow 网络**预测速度场 $v_\theta(x_t, t)$，两者的唯一差异在于推理更新公式。

*   **Baseline 推理**：`recflow.py` 使用标准 Euler 采样：
    $$ x_{t + \Delta t} = x_t + v_\theta(x_t, t)\Delta t $$
*   **势能函数定义**：`recflow_guided.py` 为球形障碍物构造软边界排斥势能。仅当轨迹点进入障碍物附近的安全区（障碍物半径 + margin）时，引导项才会生效，从而避免过远距离的无意义干预。
*   **引导型 ODE 求解**：将基础速度场修改为带有能量梯度的形式：
    $$ \frac{dx_t}{dt} = v_\theta(x_t, t) - \lambda_t \nabla_{x} E(x_t) $$
*   **动态衰减机制**：当前实现支持 `constant` 和 `linear` 两种时间衰减策略。默认采用线性衰减，使得引导在前期更强、后期更弱，以减少对最终轨迹形状的过度扰动。
*   **公平对比原则**：Base 与 Guided 版本共享同一个 checkpoint、同一个随机种子、同一个采样步数和同一个可视化流程，差异仅来自是否加入势能引导项。

## 4. 实验设计与验证
我们将通过以下严谨的消融实验（Ablation Study）来验证改进的有效性：

### 4.1 定量评价指标 (Quantitative Metrics)
1.  **避障成功率 (Success Rate, SR)**：在 1000 个随机初始化的带障碍物环境中，计算未发生碰撞的生成轨迹占比。
2.  **轨迹平滑度 (Smoothness)**：通过计算轨迹的曲率能量（Curvature Penalty）或 Fréchet 距离，评估加入能量引导后是否引发轨迹剧烈抖动。
3.  **推理耗时 (Inference Speed)**：对比传统扩散模型（100步）与我们的引导式流匹配模型（10步）的端到端生成延迟。

### 4.2 定性分析评价 (Qualitative Analysis)
开发交互式 3D 仿真环境，通过直观的视觉对比，展示 Base 模型（发生碰撞）与 Ours 模型（完美绕行）在面对相同 OOD 障碍物时的行为差异。

## 5. 项目交付与交互演示 (Demo)
当前项目包含两类可视化 / 交互入口：

*   **数据生成交互**：`data_generator.py` 基于 `Gradio + Plotly 3D` 提供专家轨迹交互生成器，可调轨迹数量、障碍物半径、序列长度等参数，并保存 `.npy` 数据集。
*   **Baseline 推理可视化**：`recflow.py` 使用 `matplotlib` 对比真实轨迹与 Rectified Flow 生成轨迹。
*   **Guided 推理可视化**：`recflow_guided.py` 在同一模型 checkpoint 上额外加入势能引导，并输出基础避障统计信息，包括 `collision_rate`、`success_rate` 和 `min_distance_to_obstacle`。

说明：当前版本的 `Gradio` 页面仍主要用于数据生成与预览，尚未整合成“网页端实时拖动障碍物并调用训练模型做避障推理”的最终统一 Demo。

## 6. 当前进展
1. 文献调研：[Flow Straight and Fast: Learning to Generate and Edit Data with Rectified Flow](http://arxiv.org/abs/2209.03003) 和 [Universal Guidance for Diffusion Models](https://arxiv.org/abs/2302.07121).  
第一篇文章核心：
![overview](./background_information/fig1.png)
![main figure](./background_information/fig2.png)  
![main alg](./background_information/fig3.png)
第二篇文章核心：
待补全。

2. Baseline 复现进展
    1. 训练数据集构建完成，参考[data_generator.py](./data_generator.py) 和 [visualize_trajectories.py](./visualize_trajectories.py)。
    2. 已复现[Rectified Flow](http://arxiv.org/abs/2209.03003)的主训练与推理流程。  
       其中，[model.py](./model.py) 定义模型架构，[train.py](./train.py) 负责训练，[recflow.py](./recflow.py) 负责 baseline 推理与可视化。
    3. 当前训练脚本已支持 `Adam` 优化器，项目已经具备从数据生成、模型训练到推理展示的闭环。

3. Energy Guidance 原型进展
    1. 已新增 [recflow_guided.py](./recflow_guided.py)，在**不重新训练模型**的前提下，为同一个 Rectified Flow checkpoint 增加推理期势能引导。
    2. 当前 guidance 版本支持：
       * 球形障碍物中心 `--obstacle-center`
       * 障碍物半径 `--obstacle-radius`
       * 引导强度 `--guidance-scale`
       * 安全边界 `--guidance-margin`
       * 时间衰减策略 `--guidance-decay {constant, linear}`
       * 引导范数裁剪 `--max-guidance-norm`
    3. 当前实现重点是构建一个**公平对比的最小原型**：Base 与 Guided 共用同一个神经网络，只在采样公式上不同。

4. 当前仍待完善的部分
    1. Guidance 在训练内障碍物场景上的提升可能不明显，更适合在 OOD 障碍物位置或半径变化场景下验证。
    2. 尚未补全系统化评测脚本，例如大规模 success rate、smoothness、inference speed 对比。
    3. 统一的交互式推理 Demo 和最终答辩展示页面仍待整合。

## 7. 推荐运行命令
建议在项目根目录下按以下顺序运行：

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 生成带碰撞过滤的训练数据
```bash
python data_generator.py --no-visualize --num-trajectories 5000 --obstacle-radius 1.0 --output-path dataset/toy_trajectories.npy
```

3. 训练 Rectified Flow baseline
```bash
python train.py --data-path dataset/toy_trajectories.npy --checkpoint-path checkpoints/rectified_flow_mlp.pt
```

4. 采样并可视化 Baseline 生成结果
```bash
python recflow.py --checkpoint-path checkpoints/rectified_flow_mlp.pt --data-path dataset/toy_trajectories.npy
```

5. 使用同一个模型进行 Energy-Guided 推理
```bash
python recflow_guided.py --checkpoint-path checkpoints/rectified_flow_mlp.pt --data-path dataset/toy_trajectories.npy
```

6. 公平对比 Base 与 Guided（推荐固定相同 seed / steps / num-samples）
```bash
python recflow.py --checkpoint-path checkpoints/rectified_flow_mlp.pt --data-path dataset/toy_trajectories.npy --seed 42 --steps 20 --num-samples 50 --save-generated outputs/base.npy --save-fig outputs/base.png --no-show

python recflow_guided.py --checkpoint-path checkpoints/rectified_flow_mlp.pt --data-path dataset/toy_trajectories.npy --seed 42 --steps 20 --num-samples 50 --save-generated outputs/guided.npy --save-fig outputs/guided.png --no-show
```

7. 在 OOD 障碍物设置下测试 Guidance（更容易观察差异）
```bash
python recflow_guided.py --checkpoint-path checkpoints/rectified_flow_mlp.pt --data-path dataset/toy_trajectories.npy --seed 42 --steps 20 --num-samples 50 --obstacle-center 0 1.5 0 --obstacle-radius 1.0 --guidance-scale 3.0 --guidance-margin 2.0 --guidance-decay constant --max-guidance-norm 10.0
```