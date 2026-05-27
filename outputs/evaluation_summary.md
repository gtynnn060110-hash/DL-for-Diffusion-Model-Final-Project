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

## Results

| Scenario | Method | Success Rate | Collision Rate | Min Distance | Smoothness | Path Length | Time (s) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| in_distribution_origin | baseline | 0.9000 | 0.1000 | 0.1206 | 0.3040 | 18.1034 | 0.0762 |
| in_distribution_origin | guided_constant | 0.9850 | 0.0150 | 0.6177 | 4.4957 | 53.0077 | 0.0785 |
| in_distribution_origin | guided_distance_gated | 0.9950 | 0.0050 | 0.7542 | 2.0130 | 36.9326 | 0.1068 |
| ood_shifted_y | baseline | 0.8550 | 0.1450 | 0.1298 | 0.3040 | 18.1034 | 0.0486 |
| ood_shifted_y | guided_constant | 1.0000 | 0.0000 | 1.4554 | 0.5742 | 22.3743 | 0.0756 |
| ood_shifted_y | guided_distance_gated | 0.9950 | 0.0050 | 0.9945 | 0.4701 | 20.5781 | 0.0959 |
| ood_double_gap | baseline | 0.6150 | 0.3850 | 0.0978 | 0.3040 | 18.1034 | 0.0442 |
| ood_double_gap | guided_constant | 0.9700 | 0.0300 | 0.8078 | 4.7778 | 52.0974 | 0.1007 |
| ood_double_gap | guided_distance_gated | 0.9300 | 0.0700 | 0.6662 | 1.8873 | 34.2087 | 0.1238 |

## Reading The Table

- `success_rate` is the primary obstacle-avoidance metric.
- `smoothness` is the mean squared second difference; lower is smoother.
- Baseline and guided use the same checkpoint, seed, sample count, integration steps, and initial noise z0.
