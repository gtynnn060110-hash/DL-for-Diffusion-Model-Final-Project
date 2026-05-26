# Evaluation Summary

## Standard Experiment

- `data_path`: `dataset/toy_trajectories.npy`
- `checkpoint_path`: `checkpoints/rectified_flow_mlp.pt`
- `device`: `cpu`
- `num_samples`: `50`
- `steps`: `20`
- `seed`: `42`
- `guidance_scale`: `3.0`
- `guidance_margin`: `2.0`
- `guidance_decay`: `constant`
- `max_guidance_norm`: `10.0`

## Results

| Scenario | Method | Success Rate | Collision Rate | Min Distance | Smoothness | Path Length | Time (s) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| in_distribution_origin | baseline | 0.9000 | 0.1000 | 0.6880 | 0.3056 | 18.0741 | 1.3465 |
| in_distribution_origin | guided | 1.0000 | 0.0000 | 1.3561 | 4.6213 | 54.0603 | 1.6049 |
| ood_shifted_y | baseline | 0.8400 | 0.1600 | 0.3201 | 0.3056 | 18.0741 | 0.5821 |
| ood_shifted_y | guided | 1.0000 | 0.0000 | 1.4554 | 0.6418 | 22.9365 | 0.5410 |

## Reading The Table

- `success_rate` is the primary obstacle-avoidance metric.
- `smoothness` is the mean squared second difference; lower is smoother.
- Baseline and guided use the same checkpoint, seed, sample count, integration steps, and initial noise z0.
