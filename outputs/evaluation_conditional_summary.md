# Evaluation Summary

## Standard Experiment

- `data_path`: `dataset/toy_trajectories.npy`
- `checkpoint_path`: `checkpoints/rectified_flow_mlp.pt`
- `conditional_checkpoint_path`: `checkpoints/rectified_flow_conditional_mlp.pt`
- `conditional_condition_dim`: `8`
- `device`: `cpu`
- `num_samples`: `200`
- `steps`: `20`
- `seed`: `42`
- `guidance_scale`: `3.0`
- `guidance_margin`: `2.0`
- `guidance_decays`: `['distance_gated']`
- `max_guidance_norm`: `10.0`
- `random_ood_count`: `0`
- `random_ood_y_range`: `[-2.5, 2.5]`
- `random_ood_z_range`: `[-1.5, 1.5]`
- `random_ood_radius_range`: `[0.8, 1.2]`
- `random_ood_min_center_norm`: `1.0`

## Results

| Scenario | Method | Success Rate | Collision Rate | Min Distance | Smoothness | Path Length | Time (s) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| in_distribution_origin | baseline | 0.7500 | 0.2500 | 0.0847 | 0.2620 | 17.2844 | 0.0273 |
| in_distribution_origin | guided_distance_gated | 0.9800 | 0.0200 | 0.6033 | 2.3036 | 38.8434 | 0.0225 |
| in_distribution_origin | conditional | 0.7450 | 0.2550 | 0.0795 | 0.2865 | 17.7527 | 0.0157 |
| in_distribution_origin | conditional_guided_distance_gated | 0.9750 | 0.0250 | 0.8475 | 2.6151 | 41.3636 | 0.0177 |
| ood_shifted_y | baseline | 0.7800 | 0.2200 | 0.1062 | 0.2620 | 17.2844 | 0.0112 |
| ood_shifted_y | guided_distance_gated | 1.0000 | 0.0000 | 1.0205 | 0.4709 | 20.2886 | 0.0156 |
| ood_shifted_y | conditional | 0.8150 | 0.1850 | 0.1949 | 0.2845 | 17.7240 | 0.0103 |
| ood_shifted_y | conditional_guided_distance_gated | 1.0000 | 0.0000 | 1.3255 | 0.4865 | 20.6979 | 0.0150 |
| ood_double_gap | baseline | 0.5750 | 0.4250 | 0.0609 | 0.2620 | 17.2844 | 0.0117 |
| ood_double_gap | guided_distance_gated | 0.9550 | 0.0450 | 0.7946 | 1.9563 | 34.8642 | 0.0203 |
| ood_double_gap | conditional | 0.7200 | 0.2800 | 0.2038 | 0.2893 | 17.8497 | 0.0122 |
| ood_double_gap | conditional_guided_distance_gated | 0.9700 | 0.0300 | 0.5774 | 1.9517 | 35.2166 | 0.0177 |

## Reading The Table

- `success_rate` is the primary obstacle-avoidance metric.
- `smoothness` is the mean squared second difference; lower is smoother.
- Unconditional and conditional methods use paired initial noise z0 within each scenario.
- Conditional methods require a conditional checkpoint and encode obstacles as flattened `(cx, cy, cz, radius)` slots.
