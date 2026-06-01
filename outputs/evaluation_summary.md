# Evaluation Summary

## Standard Experiment

- `data_path`: `dataset/toy_trajectories.npy`
- `checkpoint_path`: `checkpoints/rectified_flow_mlp.pt`
- `device`: `cpu`
- `num_samples`: `200`
- `steps`: `20`
- `seed`: `42`
- `guidance_scale`: `3.0`
- `guidance_margin`: `2.0`
- `guidance_decays`: `['constant', 'distance_gated']`
- `max_guidance_norm`: `10.0`
- `random_ood_count`: `0`
- `random_ood_y_range`: `[-2.5, 2.5]`
- `random_ood_z_range`: `[-1.5, 1.5]`
- `random_ood_radius_range`: `[0.8, 1.2]`
- `random_ood_min_center_norm`: `1.0`

## Results

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

## Reading The Table

- `success_rate` is the primary obstacle-avoidance metric.
- `smoothness` is the mean squared second difference; lower is smoother.
- Baseline and guided use the same checkpoint, seed, sample count, integration steps, and initial noise z0.
