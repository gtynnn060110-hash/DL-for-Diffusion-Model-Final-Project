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
- `random_ood_count`: `20`
- `random_ood_y_range`: `[-2.5, 2.5]`
- `random_ood_z_range`: `[-1.5, 1.5]`
- `random_ood_radius_range`: `[0.8, 1.2]`
- `random_ood_min_center_norm`: `1.0`

## Results

| Scenario | Method | Success Rate | Collision Rate | Min Distance | Smoothness | Path Length | Time (s) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| in_distribution_origin | baseline | 0.9000 | 0.1000 | 0.1206 | 0.3040 | 18.1034 | 0.1329 |
| in_distribution_origin | guided_constant | 0.9850 | 0.0150 | 0.6177 | 4.4957 | 53.0077 | 0.0971 |
| in_distribution_origin | guided_distance_gated | 0.9950 | 0.0050 | 0.7542 | 2.0130 | 36.9326 | 0.0850 |
| ood_shifted_y | baseline | 0.8550 | 0.1450 | 0.1298 | 0.3040 | 18.1034 | 0.0336 |
| ood_shifted_y | guided_constant | 1.0000 | 0.0000 | 1.4554 | 0.5742 | 22.3743 | 0.0561 |
| ood_shifted_y | guided_distance_gated | 0.9950 | 0.0050 | 0.9945 | 0.4701 | 20.5781 | 0.0811 |
| ood_double_gap | baseline | 0.6150 | 0.3850 | 0.0978 | 0.3040 | 18.1034 | 0.0397 |
| ood_double_gap | guided_constant | 0.9700 | 0.0300 | 0.8078 | 4.7778 | 52.0974 | 0.0816 |
| ood_double_gap | guided_distance_gated | 0.9300 | 0.0700 | 0.6662 | 1.8873 | 34.2087 | 0.1132 |
| random_ood_000 | baseline | 0.8950 | 0.1050 | 0.1531 | 0.3040 | 18.1034 | 0.0485 |
| random_ood_000 | guided_constant | 1.0000 | 0.0000 | 1.5734 | 0.3504 | 18.9353 | 0.0667 |
| random_ood_000 | guided_distance_gated | 1.0000 | 0.0000 | 1.2742 | 0.3247 | 18.4070 | 0.0809 |
| random_ood_001 | baseline | 0.8400 | 0.1600 | 0.1685 | 0.3040 | 18.1034 | 0.0442 |
| random_ood_001 | guided_constant | 1.0000 | 0.0000 | 2.1517 | 0.4181 | 20.2052 | 0.0671 |
| random_ood_001 | guided_distance_gated | 1.0000 | 0.0000 | 1.4767 | 0.3631 | 19.1433 | 0.0776 |
| random_ood_002 | baseline | 0.8600 | 0.1400 | 0.0539 | 0.3040 | 18.1034 | 0.0407 |
| random_ood_002 | guided_constant | 1.0000 | 0.0000 | 2.2460 | 0.3641 | 19.2230 | 0.0618 |
| random_ood_002 | guided_distance_gated | 1.0000 | 0.0000 | 1.4041 | 0.3344 | 18.5553 | 0.0815 |
| random_ood_003 | baseline | 0.8900 | 0.1100 | 0.0506 | 0.3040 | 18.1034 | 0.0427 |
| random_ood_003 | guided_constant | 1.0000 | 0.0000 | 1.3660 | 0.4541 | 20.5460 | 0.0738 |
| random_ood_003 | guided_distance_gated | 1.0000 | 0.0000 | 0.9892 | 0.3923 | 19.4093 | 0.0828 |
| random_ood_004 | baseline | 0.8900 | 0.1100 | 0.2800 | 0.3040 | 18.1034 | 0.0394 |
| random_ood_004 | guided_constant | 1.0000 | 0.0000 | 1.1656 | 1.1437 | 28.4121 | 0.0825 |
| random_ood_004 | guided_distance_gated | 0.9900 | 0.0100 | 0.9814 | 0.7902 | 24.5350 | 0.1108 |
| random_ood_005 | baseline | 0.8550 | 0.1450 | 0.0762 | 0.3040 | 18.1034 | 0.0427 |
| random_ood_005 | guided_constant | 1.0000 | 0.0000 | 1.1813 | 0.4351 | 20.3591 | 0.0672 |
| random_ood_005 | guided_distance_gated | 1.0000 | 0.0000 | 1.1150 | 0.3895 | 19.3903 | 0.0761 |
| random_ood_006 | baseline | 0.9300 | 0.0700 | 0.1120 | 0.3040 | 18.1034 | 0.0386 |
| random_ood_006 | guided_constant | 1.0000 | 0.0000 | 2.1009 | 0.3296 | 18.5600 | 0.0671 |
| random_ood_006 | guided_distance_gated | 1.0000 | 0.0000 | 1.3913 | 0.3167 | 18.2522 | 0.0894 |
| random_ood_007 | baseline | 0.7550 | 0.2450 | 0.1335 | 0.3040 | 18.1034 | 0.0412 |
| random_ood_007 | guided_constant | 1.0000 | 0.0000 | 2.3947 | 0.8969 | 26.2851 | 0.0666 |
| random_ood_007 | guided_distance_gated | 1.0000 | 0.0000 | 1.4277 | 0.6428 | 23.0809 | 0.0798 |
| random_ood_008 | baseline | 0.8600 | 0.1400 | 0.1463 | 0.3040 | 18.1034 | 0.0378 |
| random_ood_008 | guided_constant | 1.0000 | 0.0000 | 1.9610 | 0.4773 | 20.9808 | 0.0584 |
| random_ood_008 | guided_distance_gated | 1.0000 | 0.0000 | 1.2140 | 0.4075 | 19.6956 | 0.0675 |
| random_ood_009 | baseline | 0.8000 | 0.2000 | 0.1250 | 0.3040 | 18.1034 | 0.0478 |
| random_ood_009 | guided_constant | 1.0000 | 0.0000 | 1.3542 | 1.3173 | 30.1954 | 0.0630 |
| random_ood_009 | guided_distance_gated | 0.9950 | 0.0050 | 0.8335 | 0.9106 | 25.9016 | 0.0762 |
| random_ood_010 | baseline | 0.8700 | 0.1300 | 0.0512 | 0.3040 | 18.1034 | 0.0532 |
| random_ood_010 | guided_constant | 1.0000 | 0.0000 | 1.6194 | 0.4107 | 19.9242 | 0.0704 |
| random_ood_010 | guided_distance_gated | 1.0000 | 0.0000 | 1.0402 | 0.3676 | 19.0388 | 0.1121 |
| random_ood_011 | baseline | 0.9200 | 0.0800 | 0.4170 | 0.3040 | 18.1034 | 0.0597 |
| random_ood_011 | guided_constant | 1.0000 | 0.0000 | 2.4808 | 0.3172 | 18.2619 | 0.0906 |
| random_ood_011 | guided_distance_gated | 1.0000 | 0.0000 | 1.7831 | 0.3043 | 17.9868 | 0.0804 |
| random_ood_012 | baseline | 0.9450 | 0.0550 | 0.1711 | 0.3040 | 18.1034 | 0.0447 |
| random_ood_012 | guided_constant | 1.0000 | 0.0000 | 2.1010 | 0.3164 | 18.1646 | 0.0602 |
| random_ood_012 | guided_distance_gated | 1.0000 | 0.0000 | 1.5520 | 0.3066 | 18.0154 | 0.0840 |
| random_ood_013 | baseline | 0.9150 | 0.0850 | 0.2204 | 0.3040 | 18.1034 | 0.0542 |
| random_ood_013 | guided_constant | 1.0000 | 0.0000 | 1.1267 | 0.8853 | 25.6516 | 0.0857 |
| random_ood_013 | guided_distance_gated | 0.9900 | 0.0100 | 0.7621 | 0.6233 | 22.5324 | 0.0838 |
| random_ood_014 | baseline | 0.8450 | 0.1550 | 0.2396 | 0.3040 | 18.1034 | 0.0502 |
| random_ood_014 | guided_constant | 1.0000 | 0.0000 | 1.2357 | 0.9035 | 26.3285 | 0.0612 |
| random_ood_014 | guided_distance_gated | 0.9850 | 0.0150 | 0.8162 | 0.6863 | 23.3710 | 0.0761 |
| random_ood_015 | baseline | 0.9000 | 0.1000 | 0.2364 | 0.3040 | 18.1034 | 0.0372 |
| random_ood_015 | guided_constant | 1.0000 | 0.0000 | 2.0603 | 0.3358 | 18.5164 | 0.0614 |
| random_ood_015 | guided_distance_gated | 1.0000 | 0.0000 | 1.4722 | 0.3165 | 18.1763 | 0.0870 |
| random_ood_016 | baseline | 0.8350 | 0.1650 | 0.1454 | 0.3040 | 18.1034 | 0.0609 |
| random_ood_016 | guided_constant | 0.9950 | 0.0050 | 1.1171 | 1.0616 | 28.2114 | 0.0956 |
| random_ood_016 | guided_distance_gated | 1.0000 | 0.0000 | 1.3308 | 0.7262 | 24.1690 | 0.1076 |
| random_ood_017 | baseline | 0.9200 | 0.0800 | 0.2782 | 0.3040 | 18.1034 | 0.0489 |
| random_ood_017 | guided_constant | 1.0000 | 0.0000 | 0.9592 | 0.6564 | 23.3026 | 0.0845 |
| random_ood_017 | guided_distance_gated | 0.9950 | 0.0050 | 0.6293 | 0.5126 | 21.1890 | 0.0923 |
| random_ood_018 | baseline | 0.8450 | 0.1550 | 0.1656 | 0.3040 | 18.1034 | 0.0429 |
| random_ood_018 | guided_constant | 0.9950 | 0.0050 | 1.0319 | 1.1396 | 28.3019 | 0.0725 |
| random_ood_018 | guided_distance_gated | 0.9950 | 0.0050 | 1.0938 | 0.7663 | 24.4011 | 0.0847 |
| random_ood_019 | baseline | 0.8950 | 0.1050 | 0.1365 | 0.3040 | 18.1034 | 0.0402 |
| random_ood_019 | guided_constant | 1.0000 | 0.0000 | 1.5332 | 0.3250 | 18.4898 | 0.0614 |
| random_ood_019 | guided_distance_gated | 1.0000 | 0.0000 | 1.3676 | 0.3088 | 18.1189 | 0.0939 |

## Random OOD Summary

| Method | Success Rate | Collision Rate | Min Distance | Smoothness | Path Length | Time (s) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 0.8732 | 0.1267 | 0.1680 | 0.3040 | 18.1034 | 0.0458 |
| guided_constant | 0.9995 | 0.0005 | 1.6380 | 0.6269 | 22.4427 | 0.0709 |
| guided_distance_gated | 0.9975 | 0.0025 | 1.1977 | 0.4895 | 20.6685 | 0.0862 |

## Reading The Table

- `success_rate` is the primary obstacle-avoidance metric.
- `smoothness` is the mean squared second difference; lower is smoother.
- Baseline and guided use the same checkpoint, seed, sample count, integration steps, and initial noise z0.
