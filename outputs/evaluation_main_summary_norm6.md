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
- `guidance_decays`: `['constant', 'distance_gated']`
- `max_guidance_norm`: `6.0`
- `random_ood_count`: `0`
- `random_ood_y_range`: `[-2.5, 2.5]`
- `random_ood_z_range`: `[-1.5, 1.5]`
- `random_ood_radius_range`: `[0.8, 1.2]`
- `random_ood_min_center_norm`: `1.0`

## Results

| Scenario | Method | Success Rate | Collision Rate | Min Distance | Smoothness | Path Length | Time (s) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| in_distribution_origin | baseline | 0.9000 | 0.1000 | 0.1206 | 0.3040 | 18.1034 | 0.0746 |
| in_distribution_origin | guided_constant | 0.9850 | 0.0150 | 0.5609 | 4.4308 | 52.6372 | 0.0815 |
| in_distribution_origin | guided_distance_gated | 0.9950 | 0.0050 | 0.6793 | 1.9884 | 36.7335 | 0.1078 |
| in_distribution_origin | conditional | 0.7800 | 0.2200 | 0.1241 | 0.2981 | 17.8493 | 0.0654 |
| in_distribution_origin | conditional_guided_constant | 0.9900 | 0.0100 | 0.8761 | 7.4136 | 66.4090 | 0.1069 |
| in_distribution_origin | conditional_guided_distance_gated | 0.9800 | 0.0200 | 0.6594 | 2.9661 | 43.2668 | 0.1304 |
| ood_shifted_y | baseline | 0.8550 | 0.1450 | 0.1298 | 0.3040 | 18.1034 | 0.0582 |
| ood_shifted_y | guided_constant | 1.0000 | 0.0000 | 1.4497 | 0.5708 | 22.3320 | 0.0840 |
| ood_shifted_y | guided_distance_gated | 0.9950 | 0.0050 | 0.9958 | 0.4677 | 20.5474 | 0.1066 |
| ood_shifted_y | conditional | 0.9100 | 0.0900 | 0.3067 | 0.2975 | 17.8371 | 0.0630 |
| ood_shifted_y | conditional_guided_constant | 1.0000 | 0.0000 | 2.0448 | 0.6572 | 23.4272 | 0.1013 |
| ood_shifted_y | conditional_guided_distance_gated | 1.0000 | 0.0000 | 1.4835 | 0.5004 | 21.0857 | 0.1067 |
| ood_double_gap | baseline | 0.6150 | 0.3850 | 0.0978 | 0.3040 | 18.1034 | 0.0475 |
| ood_double_gap | guided_constant | 0.9750 | 0.0250 | 0.8103 | 4.7382 | 51.8769 | 0.1032 |
| ood_double_gap | guided_distance_gated | 0.9250 | 0.0750 | 0.6643 | 1.8744 | 34.0986 | 0.1320 |
| ood_double_gap | conditional | 0.6750 | 0.3250 | 0.0769 | 0.2994 | 17.8968 | 0.0489 |
| ood_double_gap | conditional_guided_constant | 0.9900 | 0.0100 | 0.6006 | 7.4461 | 64.3279 | 0.1023 |
| ood_double_gap | conditional_guided_distance_gated | 0.9750 | 0.0250 | 0.7611 | 2.3190 | 37.4667 | 0.1195 |

## Reading The Table

- `success_rate` is the primary obstacle-avoidance metric.
- `smoothness` is the mean squared second difference; lower is smoother.
- Unconditional and conditional methods use paired initial noise z0 within each scenario.
- Conditional methods require a conditional checkpoint and encode obstacles as flattened `(cx, cy, cz, radius)` slots.
