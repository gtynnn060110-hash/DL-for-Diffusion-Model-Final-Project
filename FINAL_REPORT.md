# Rectified Flow for 3D Trajectory Generation with Obstacle-Aware Guidance

## Abstract

This project studies Rectified Flow for generating three-dimensional trajectories under obstacle-avoidance constraints. Starting from a basic generative trajectory model, we build a complete pipeline that generates synthetic expert trajectories, trains a Rectified Flow velocity field, and samples new trajectories with Euler integration. We then improve out-of-distribution obstacle avoidance through two complementary strategies: inference-time energy guidance and training-time conditional modeling.

The first strategy adds a differentiable spherical obstacle repulsion term during sampling, without retraining the model. We compare constant guidance with a distance-gated variant that activates only near obstacles. The second strategy trains a conditional Rectified Flow model whose velocity field receives explicit obstacle parameters as input. Experiments show that energy guidance is highly effective for OOD obstacle layouts, increasing success rates from 0.780 to 1.000 in a shifted-obstacle scenario and from 0.575 to 0.955 in a double-obstacle scenario. Conditional modeling improves the unguided baseline on OOD cases, especially in the double-obstacle setting, where success rises from 0.575 to 0.720. Combining both ideas gives the strongest overall result, reaching 0.970 success in the double-obstacle scenario.

## 1. Introduction

Generative models are commonly discussed in the context of images, audio, or text, but the same ideas can also be applied to continuous motion generation. In this project, the target distribution is a set of smooth 3D trajectories connecting a fixed start point to a fixed goal point while avoiding obstacles. This setting is small enough to analyze carefully, but still exposes an important limitation of purely data-driven generative models: a model trained on one obstacle layout may fail when the obstacle configuration changes at inference time.

We choose Rectified Flow as the base generative framework because it provides a simple and efficient continuous-time formulation. Instead of learning a long reverse diffusion chain, Rectified Flow learns a velocity field that transports Gaussian noise to data samples along a straight interpolation path. In practice, high-quality samples can be generated with a small number of Euler steps, which is attractive for trajectory generation.

The project is organized around three questions:

1. Can a simple Rectified Flow model learn a smooth 3D trajectory distribution?
2. Can inference-time physical guidance improve obstacle avoidance without retraining?
3. Can a conditional model internalize obstacle information and complement inference-time guidance?

## 2. Method

### 2.1 Rectified Flow for Trajectory Generation

Rectified Flow learns a velocity field that maps a noise sample \(x_0\) to a data sample \(x_1\). During training, we sample a time \(t \in [0, 1]\) and construct the linear interpolation

\[
x_t = (1 - t)x_0 + t x_1 .
\]

The model is trained to predict the constant target velocity

\[
u_t = x_1 - x_0 .
\]

The training objective is

\[
\mathcal{L} = \mathbb{E}_{x_0, x_1, t}\left[\|v_\theta(x_t, t) - (x_1 - x_0)\|_2^2\right].
\]

At inference time, a trajectory is initialized from Gaussian noise and updated by Euler integration:

\[
z_{k+1} = z_k + v_\theta(z_k, t_k)\Delta t .
\]

In this project, each trajectory has 50 time steps and each point is 3-dimensional, so the flattened trajectory dimension is 150.

The training data consists of synthetic expert trajectories. Each trajectory starts from \((-5, 0, 0)\) and ends at \((5, 0, 0)\). The path is generated from cubic Bezier control points and then filtered to avoid a spherical obstacle. This creates a smooth trajectory distribution with a clear geometric constraint.

### 2.2 Model Architecture

The base model is an MLP velocity network. A sinusoidal time embedding is concatenated with the flattened trajectory input, and the network predicts a velocity vector with the same shape as the trajectory.

Two variants are implemented:

| Variant | Forward Form | Input Components | Condition |
| --- | --- | --- | --- |
| Unconditional Rectified Flow | \(v_\theta(x, t)\) | trajectory + time embedding | none |
| Conditional Rectified Flow | \(v_\theta(x, t, c)\) | trajectory + time embedding + obstacle vector | obstacle parameters |

For the unconditional model, the dataset contains only trajectories. For the conditional model, the dataset is stored as an `.npz` file containing both trajectories and obstacle parameters. Each obstacle is represented by center coordinates and radius:

\[
(c_x, c_y, c_z, r).
\]

The conditional experiments support up to two obstacles, so the condition vector is

\[
c = [c_{x1}, c_{y1}, c_{z1}, r_1, c_{x2}, c_{y2}, c_{z2}, r_2].
\]

Unused obstacle slots are zero-padded, with radius zero indicating an inactive obstacle. The conditional model uses simple concatenation rather than cross-attention or classifier-free guidance. This is a deliberate design choice: the condition vector is only 8-dimensional, so direct concatenation is sufficient for this small-scale geometric setting.

### 2.3 Obstacle-Aware Energy Guidance

The unconditional baseline learns the training trajectory distribution, but it does not explicitly know the obstacle layout at inference time. To improve robustness under new obstacle configurations, we add an obstacle energy term during sampling.

For a spherical obstacle, the energy increases when trajectory points enter or approach the obstacle margin. The guidance gradient is computed with respect to trajectory points and subtracted from the learned velocity:

\[
z_{k+1} = z_k + \left(v_\theta(z_k, t_k) - \lambda \nabla E(z_k)\right)\Delta t .
\]

Here \(\lambda\) is the guidance scale. The implementation also supports clipping the guidance norm to avoid unstable updates.

We evaluate two guidance modes:

| Mode | Description |
| --- | --- |
| `constant` | Applies obstacle repulsion throughout the whole sampling process. |
| `distance_gated` | Activates guidance only when the trajectory enters a margin around the obstacle. |

The distance-gated version is intended to reduce unnecessary perturbations when the generated trajectory is already far from obstacles. Multi-obstacle scenes are handled by summing gradients across obstacles, while the distance gate uses the maximum activation across obstacles.

## 3. Experimental Setup

### 3.1 Scenarios and Metrics

The main evaluation uses three scenarios:

| Scenario | Description |
| --- | --- |
| `in_distribution_origin` | Single obstacle at the training-like origin location. |
| `ood_shifted_y` | Single obstacle shifted along the \(y\)-axis. |
| `ood_double_gap` | Two obstacles placed at \(y = 1.5\) and \(y = -1.5\), creating a harder double-gap setting. |

The primary metric is success rate, defined as the fraction of trajectories that avoid collision with all obstacles. We also report collision rate, minimum distance to obstacles, smoothness, path length, and runtime.

### 3.2 Implementation Details

The standard experiment uses:

| Parameter | Value |
| --- | ---: |
| Number of samples | 200 |
| Sampling steps | 20 |
| Guidance scale | 3.0 |
| Guidance margin | 2.0 |
| Max guidance norm | 10.0 |
| Device | CPU |
| Seed | 42 |

A key evaluation detail is paired-noise comparison. Within each scenario, baseline, guided, conditional, and conditional-guided methods are initialized from the same sampled noise \(z_0\). Therefore, differences between methods are caused by the method itself rather than random initialization variance.

## 4. Results and Analysis

### 4.1 Main Comparison

The full evaluation compares four methods:

1. Unconditional baseline
2. Unconditional model with distance-gated guidance
3. Conditional Rectified Flow
4. Conditional Rectified Flow with distance-gated guidance

| Scenario | Method | Success Rate | Collision Rate | Min Distance | Smoothness | Path Length |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| in_distribution_origin | baseline | 0.750 | 0.250 | 0.085 | 0.262 | 17.284 |
| in_distribution_origin | guided_distance_gated | 0.980 | 0.020 | 0.603 | 2.304 | 38.843 |
| in_distribution_origin | conditional | 0.745 | 0.255 | 0.080 | 0.287 | 17.753 |
| in_distribution_origin | conditional_guided_distance_gated | 0.975 | 0.025 | 0.848 | 2.615 | 41.364 |
| ood_shifted_y | baseline | 0.780 | 0.220 | 0.106 | 0.262 | 17.284 |
| ood_shifted_y | guided_distance_gated | 1.000 | 0.000 | 1.021 | 0.471 | 20.289 |
| ood_shifted_y | conditional | 0.815 | 0.185 | 0.195 | 0.285 | 17.724 |
| ood_shifted_y | conditional_guided_distance_gated | 1.000 | 0.000 | 1.326 | 0.487 | 20.698 |
| ood_double_gap | baseline | 0.575 | 0.425 | 0.061 | 0.262 | 17.284 |
| ood_double_gap | guided_distance_gated | 0.955 | 0.045 | 0.795 | 1.956 | 34.864 |
| ood_double_gap | conditional | 0.720 | 0.280 | 0.204 | 0.289 | 17.850 |
| ood_double_gap | conditional_guided_distance_gated | 0.970 | 0.030 | 0.577 | 1.952 | 35.217 |

The results show three important patterns. First, inference-time guidance is the strongest single intervention. In the shifted OOD scenario, success improves from 0.780 to 1.000. In the double-obstacle scenario, success improves from 0.575 to 0.955.

Second, conditional training improves robustness even without guidance. In the shifted scenario, the conditional model improves success from 0.780 to 0.815. In the harder double-obstacle scenario, it improves success from 0.575 to 0.720, a gain of 14.5 percentage points.

Third, conditional modeling and guidance are complementary. The best overall result is conditional plus distance-gated guidance, which reaches 0.970 success in the double-obstacle scenario.

### 4.2 Guidance Ablation

An earlier unconditional evaluation compared the baseline, constant guidance, and distance-gated guidance:

| Scenario | Baseline | Guided Constant | Guided Distance-Gated |
| --- | ---: | ---: | ---: |
| in_distribution_origin | 0.900 | 0.985 | 0.995 |
| ood_shifted_y | 0.855 | 1.000 | 0.995 |
| ood_double_gap | 0.615 | 0.970 | 0.930 |

Constant guidance can produce slightly higher success in the hardest double-obstacle setting, but it tends to perturb trajectories more strongly. Distance-gated guidance is therefore the preferred default because it preserves most of the obstacle-avoidance benefit while reducing unnecessary trajectory distortion.

We also sweep three guidance parameters: `guidance_scale`, `guidance_margin`, and `max_guidance_norm`. The scale sweep uses 500 samples across the same three scenarios. The main findings are:

- Increasing `guidance_scale` generally improves success rate, but also increases smoothness cost and path length.
- `guidance_scale = 3.0` is a practical balance point: OOD success is near-perfect in the shifted scenario and strong in the double-obstacle scenario, without the extreme path length growth observed at scale 5.0.
- `guidance_margin = 2.0` is important for robust OOD avoidance. Smaller margins are less reliable, especially in the double-obstacle setting.
- `max_guidance_norm = 10.0` is a safe default. It is high enough not to over-constrain useful gradients but still prevents unusually large updates.
- Conditional models often achieve comparable success with slightly lower effective guidance pressure, suggesting that training-time conditioning and inference-time guidance reinforce each other.

Based on these observations, the recommended default configuration is:

| Parameter | Value |
| --- | ---: |
| `guidance_scale` | 3.0 |
| `guidance_margin` | 2.0 |
| `max_guidance_norm` | 10.0 |
| `guidance_decay` | `distance_gated` |

### 4.3 Discussion

The experiments suggest that Rectified Flow is a suitable framework for small-scale continuous trajectory generation. It can learn smooth expert-like trajectories and generate samples with only 20 Euler steps. However, the unconditional model is limited by the training distribution. When obstacles move or multiple obstacles appear, the model may produce trajectories that remain plausible under the training distribution but collide with the new environment.

Energy guidance addresses this issue by injecting an explicit geometric constraint during sampling. This is effective because obstacle avoidance has a clear differentiable structure in this simplified setting. The method is also model-agnostic: the same obstacle-gradient function can be applied to both unconditional and conditional samplers.

The conditional model provides a different type of improvement. By exposing obstacle parameters during training, the model can learn obstacle-aware behavior directly. Conditional modeling alone does not match guided sampling, but it improves OOD performance while preserving relatively short and smooth trajectories. The best behavior comes from combining both approaches: conditioning provides global obstacle context, and guidance enforces local physical clearance during sampling.

The repository contains several generated figures that can be included in the final submission:

| Figure File | Suggested Use |
| --- | --- |
| `outputs/base_ood.png` | Baseline generation under a shifted obstacle. |
| `outputs/guided_distance_gated_ood.png` | Distance-gated guidance in the shifted OOD setting. |
| `outputs/guided_distance_gated_double_ood.png` | Guided generation in the double-obstacle setting. |
| `outputs/conditional_ood.png` | Conditional model without guidance. |
| `outputs/conditional_guided_ood.png` | Conditional model with guidance. |
| `outputs/ablation_plots/*.png` | Parameter-sweep curves for guidance scale, margin, and norm. |

## 5. Limitations and Future Work

This project makes several simplifying assumptions:

- Obstacles are static spheres with soft distance-based boundaries.
- The model generates complete trajectories as flattened vectors rather than using an autoregressive or sequence-aware architecture.
- The conditional representation is a simple fixed-length vector and supports only up to two obstacles in the current experiments.
- Energy guidance is an inference-time heuristic, not a learned global planner.
- Strong guidance can increase path length and reduce smoothness, especially with constant guidance.
- The experiments use synthetic Bezier trajectories rather than real robot or vehicle motion data.

Several extensions are natural: classifier-free guidance for conditional Rectified Flow, more expressive obstacle representations such as signed distance fields or occupancy grids, sequence-aware architectures such as temporal Transformers, dynamic obstacles with time-dependent constraints, and evaluation on more realistic motion-planning or robotics datasets.

## 6. Conclusion

This project builds a complete Rectified Flow pipeline for 3D trajectory generation and studies how to improve obstacle avoidance under distribution shift. The unconditional model can generate smooth trajectories, but it is not reliable when obstacle configurations change. Inference-time energy guidance substantially improves OOD safety without retraining, while distance-gated guidance reduces unnecessary perturbation compared with always-on guidance. Conditional Rectified Flow further improves robustness by giving the model explicit obstacle context during training.

The central conclusion is that training-time conditioning and inference-time guidance are complementary. Conditioning helps the model internalize obstacle-aware trajectory structure, while guidance provides precise local constraint enforcement during sampling. Their combination achieves the best overall performance, especially in the hardest double-obstacle scenario.
