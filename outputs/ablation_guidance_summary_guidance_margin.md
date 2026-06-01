# Guidance Ablation Summary

## Sweep Configuration

- `data_path`: `dataset/toy_trajectories.npy`
- `checkpoint_path`: `checkpoints/rectified_flow_mlp.pt`
- `device`: `cpu`
- `num_samples`: `500`
- `steps`: `20`
- `seed`: `42`
- `ablate`: `guidance_margin`
- `values`: `[0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5]`
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

| Scenario | Decay | Param | Value | Success Rate | Collision Rate | Min Distance | Smoothness | Path Length | Time (s) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| in_distribution_origin | baseline | guidance_margin | 0.0000 | 0.7280 | 0.2720 | 0.0735 | 0.2692 | 17.4148 | 0.0241 |
| in_distribution_origin | constant | guidance_margin | 0.0000 | 0.7460 | 0.2540 | 0.2232 | 0.2954 | 17.8878 | 0.0257 |
| in_distribution_origin | constant | guidance_margin | 0.2500 | 0.7720 | 0.2280 | 0.3054 | 0.3368 | 18.5920 | 0.0296 |
| in_distribution_origin | constant | guidance_margin | 0.5000 | 0.8060 | 0.1940 | 0.4107 | 0.4168 | 19.8624 | 0.0264 |
| in_distribution_origin | constant | guidance_margin | 0.7500 | 0.8240 | 0.1760 | 0.2881 | 0.5603 | 21.9359 | 0.0250 |
| in_distribution_origin | constant | guidance_margin | 1.0000 | 0.8380 | 0.1620 | 0.3840 | 0.8084 | 25.0986 | 0.0262 |
| in_distribution_origin | constant | guidance_margin | 1.2500 | 0.8860 | 0.1140 | 0.4407 | 1.2313 | 29.7149 | 0.0256 |
| in_distribution_origin | constant | guidance_margin | 1.5000 | 0.9400 | 0.0600 | 0.3592 | 1.9581 | 36.2675 | 0.0263 |
| in_distribution_origin | constant | guidance_margin | 1.7500 | 0.9760 | 0.0240 | 0.4910 | 3.2122 | 45.3236 | 0.0266 |
| in_distribution_origin | constant | guidance_margin | 2.0000 | 0.9820 | 0.0180 | 0.6567 | 5.3367 | 57.4689 | 0.0257 |
| in_distribution_origin | constant | guidance_margin | 2.5000 | 0.9900 | 0.0100 | 0.8358 | 14.1209 | 92.4387 | 0.0271 |
| in_distribution_origin | distance_gated | guidance_margin | 0.0000 | 0.7460 | 0.2540 | 0.2232 | 0.2954 | 17.8878 | 0.0332 |
| in_distribution_origin | distance_gated | guidance_margin | 0.2500 | 0.7700 | 0.2300 | 0.3110 | 0.3335 | 18.5293 | 0.0275 |
| in_distribution_origin | distance_gated | guidance_margin | 0.5000 | 0.8080 | 0.1920 | 0.4121 | 0.3971 | 19.5271 | 0.0274 |
| in_distribution_origin | distance_gated | guidance_margin | 0.7500 | 0.8180 | 0.1820 | 0.3778 | 0.4954 | 20.9675 | 0.0292 |
| in_distribution_origin | distance_gated | guidance_margin | 1.0000 | 0.8440 | 0.1560 | 0.3711 | 0.6429 | 22.9604 | 0.0282 |
| in_distribution_origin | distance_gated | guidance_margin | 1.2500 | 0.8700 | 0.1300 | 0.4854 | 0.8618 | 25.6442 | 0.0291 |
| in_distribution_origin | distance_gated | guidance_margin | 1.5000 | 0.9120 | 0.0880 | 0.5521 | 1.1874 | 29.1919 | 0.0290 |
| in_distribution_origin | distance_gated | guidance_margin | 1.7500 | 0.9480 | 0.0520 | 0.5187 | 1.6762 | 33.8217 | 0.0285 |
| in_distribution_origin | distance_gated | guidance_margin | 2.0000 | 0.9800 | 0.0200 | 0.6033 | 2.4153 | 39.7850 | 0.0288 |
| in_distribution_origin | distance_gated | guidance_margin | 2.5000 | 0.9900 | 0.0100 | 0.5786 | 5.1828 | 56.7460 | 0.0287 |
| ood_shifted_y | baseline | guidance_margin | 0.0000 | 0.7620 | 0.2380 | 0.0767 | 0.2692 | 17.4148 | 0.0228 |
| ood_shifted_y | constant | guidance_margin | 0.0000 | 0.7760 | 0.2240 | 0.2172 | 0.2755 | 17.5063 | 0.0273 |
| ood_shifted_y | constant | guidance_margin | 0.2500 | 0.8200 | 0.1800 | 0.2706 | 0.2853 | 17.6377 | 0.0257 |
| ood_shifted_y | constant | guidance_margin | 0.5000 | 0.8680 | 0.1320 | 0.2982 | 0.3026 | 17.8648 | 0.0264 |
| ood_shifted_y | constant | guidance_margin | 0.7500 | 0.9100 | 0.0900 | 0.3387 | 0.3282 | 18.2041 | 0.0266 |
| ood_shifted_y | constant | guidance_margin | 1.0000 | 0.9500 | 0.0500 | 0.6156 | 0.3616 | 18.6660 | 0.0267 |
| ood_shifted_y | constant | guidance_margin | 1.2500 | 0.9840 | 0.0160 | 0.6031 | 0.4021 | 19.2727 | 0.0262 |
| ood_shifted_y | constant | guidance_margin | 1.5000 | 0.9940 | 0.0060 | 0.8016 | 0.4545 | 20.0903 | 0.0261 |
| ood_shifted_y | constant | guidance_margin | 1.7500 | 1.0000 | 0.0000 | 1.0223 | 0.5239 | 21.1946 | 0.0265 |
| ood_shifted_y | constant | guidance_margin | 2.0000 | 1.0000 | 0.0000 | 1.4181 | 0.6249 | 22.6936 | 0.0269 |
| ood_shifted_y | constant | guidance_margin | 2.5000 | 1.0000 | 0.0000 | 1.2913 | 0.9970 | 27.3816 | 0.0261 |
| ood_shifted_y | distance_gated | guidance_margin | 0.0000 | 0.7760 | 0.2240 | 0.2172 | 0.2755 | 17.5063 | 0.0284 |
| ood_shifted_y | distance_gated | guidance_margin | 0.2500 | 0.8160 | 0.1840 | 0.2788 | 0.2850 | 17.6336 | 0.0297 |
| ood_shifted_y | distance_gated | guidance_margin | 0.5000 | 0.8640 | 0.1360 | 0.2894 | 0.2998 | 17.8253 | 0.0290 |
| ood_shifted_y | distance_gated | guidance_margin | 0.7500 | 0.8980 | 0.1020 | 0.3242 | 0.3197 | 18.0777 | 0.0298 |
| ood_shifted_y | distance_gated | guidance_margin | 1.0000 | 0.9280 | 0.0720 | 0.4883 | 0.3437 | 18.3895 | 0.0287 |
| ood_shifted_y | distance_gated | guidance_margin | 1.2500 | 0.9540 | 0.0460 | 0.6322 | 0.3711 | 18.7675 | 0.0289 |
| ood_shifted_y | distance_gated | guidance_margin | 1.5000 | 0.9880 | 0.0120 | 0.6428 | 0.4022 | 19.2298 | 0.0297 |
| ood_shifted_y | distance_gated | guidance_margin | 1.7500 | 0.9940 | 0.0060 | 0.7768 | 0.4403 | 19.8202 | 0.0288 |
| ood_shifted_y | distance_gated | guidance_margin | 2.0000 | 0.9980 | 0.0020 | 0.4836 | 0.4882 | 20.5759 | 0.0296 |
| ood_shifted_y | distance_gated | guidance_margin | 2.5000 | 1.0000 | 0.0000 | 1.3279 | 0.6305 | 22.7367 | 0.0276 |
| ood_double_gap | baseline | guidance_margin | 0.0000 | 0.5580 | 0.4420 | 0.0609 | 0.2692 | 17.4148 | 0.0222 |
| ood_double_gap | constant | guidance_margin | 0.0000 | 0.5820 | 0.4180 | 0.1619 | 0.2821 | 17.6069 | 0.0284 |
| ood_double_gap | constant | guidance_margin | 0.2500 | 0.6580 | 0.3420 | 0.2792 | 0.3015 | 17.8812 | 0.0273 |
| ood_double_gap | constant | guidance_margin | 0.5000 | 0.7360 | 0.2640 | 0.3935 | 0.3387 | 18.4012 | 0.0288 |
| ood_double_gap | constant | guidance_margin | 0.7500 | 0.8140 | 0.1860 | 0.2662 | 0.4039 | 19.3099 | 0.0287 |
| ood_double_gap | constant | guidance_margin | 1.0000 | 0.8740 | 0.1260 | 0.5538 | 0.5215 | 20.9085 | 0.0296 |
| ood_double_gap | constant | guidance_margin | 1.2500 | 0.9060 | 0.0940 | 0.5171 | 0.7716 | 23.9420 | 0.0282 |
| ood_double_gap | constant | guidance_margin | 1.5000 | 0.9480 | 0.0520 | 0.5363 | 1.3352 | 29.5697 | 0.0288 |
| ood_double_gap | constant | guidance_margin | 1.7500 | 0.9640 | 0.0360 | 0.5660 | 2.6180 | 39.4753 | 0.0289 |
| ood_double_gap | constant | guidance_margin | 2.0000 | 0.9620 | 0.0380 | 0.6463 | 5.4441 | 55.5771 | 0.0291 |
| ood_double_gap | constant | guidance_margin | 2.5000 | 0.9880 | 0.0120 | 0.5917 | 20.4519 | 108.4721 | 0.0284 |
| ood_double_gap | distance_gated | guidance_margin | 0.0000 | 0.5820 | 0.4180 | 0.1619 | 0.2821 | 17.6069 | 0.0329 |
| ood_double_gap | distance_gated | guidance_margin | 0.2500 | 0.6480 | 0.3520 | 0.2757 | 0.3007 | 17.8688 | 0.0327 |
| ood_double_gap | distance_gated | guidance_margin | 0.5000 | 0.7160 | 0.2840 | 0.3812 | 0.3313 | 18.2874 | 0.0330 |
| ood_double_gap | distance_gated | guidance_margin | 0.7500 | 0.7820 | 0.2180 | 0.3713 | 0.3768 | 18.9019 | 0.0330 |
| ood_double_gap | distance_gated | guidance_margin | 1.0000 | 0.8400 | 0.1600 | 0.2868 | 0.4435 | 19.8073 | 0.0330 |
| ood_double_gap | distance_gated | guidance_margin | 1.2500 | 0.8700 | 0.1300 | 0.5830 | 0.5576 | 21.3146 | 0.0322 |
| ood_double_gap | distance_gated | guidance_margin | 1.5000 | 0.9100 | 0.0900 | 0.5057 | 0.7786 | 23.9455 | 0.0328 |
| ood_double_gap | distance_gated | guidance_margin | 1.7500 | 0.9420 | 0.0580 | 0.5017 | 1.2132 | 28.3924 | 0.0330 |
| ood_double_gap | distance_gated | guidance_margin | 2.0000 | 0.9480 | 0.0520 | 0.7318 | 2.0695 | 35.5963 | 0.0319 |
| ood_double_gap | distance_gated | guidance_margin | 2.5000 | 0.9740 | 0.0260 | 0.6643 | 6.7394 | 62.0656 | 0.0327 |

## Scenario Mean Summary

| Scenario | Decay | Param | Value | Success Rate | Collision Rate | Min Distance | Smoothness | Path Length | Time (s) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| in_distribution_origin | baseline | guidance_margin | 0.0000 | 0.7280 | 0.2720 | 0.0735 | 0.2692 | 17.4148 | 0.0241 |
| in_distribution_origin | constant | guidance_margin | 0.0000 | 0.7460 | 0.2540 | 0.2232 | 0.2954 | 17.8878 | 0.0257 |
| in_distribution_origin | constant | guidance_margin | 0.2500 | 0.7720 | 0.2280 | 0.3054 | 0.3368 | 18.5920 | 0.0296 |
| in_distribution_origin | constant | guidance_margin | 0.5000 | 0.8060 | 0.1940 | 0.4107 | 0.4168 | 19.8624 | 0.0264 |
| in_distribution_origin | constant | guidance_margin | 0.7500 | 0.8240 | 0.1760 | 0.2881 | 0.5603 | 21.9359 | 0.0250 |
| in_distribution_origin | constant | guidance_margin | 1.0000 | 0.8380 | 0.1620 | 0.3840 | 0.8084 | 25.0986 | 0.0262 |
| in_distribution_origin | constant | guidance_margin | 1.2500 | 0.8860 | 0.1140 | 0.4407 | 1.2313 | 29.7149 | 0.0256 |
| in_distribution_origin | constant | guidance_margin | 1.5000 | 0.9400 | 0.0600 | 0.3592 | 1.9581 | 36.2675 | 0.0263 |
| in_distribution_origin | constant | guidance_margin | 1.7500 | 0.9760 | 0.0240 | 0.4910 | 3.2122 | 45.3236 | 0.0266 |
| in_distribution_origin | constant | guidance_margin | 2.0000 | 0.9820 | 0.0180 | 0.6567 | 5.3367 | 57.4689 | 0.0257 |
| in_distribution_origin | constant | guidance_margin | 2.5000 | 0.9900 | 0.0100 | 0.8358 | 14.1209 | 92.4387 | 0.0271 |
| in_distribution_origin | distance_gated | guidance_margin | 0.0000 | 0.7460 | 0.2540 | 0.2232 | 0.2954 | 17.8878 | 0.0332 |
| in_distribution_origin | distance_gated | guidance_margin | 0.2500 | 0.7700 | 0.2300 | 0.3110 | 0.3335 | 18.5293 | 0.0275 |
| in_distribution_origin | distance_gated | guidance_margin | 0.5000 | 0.8080 | 0.1920 | 0.4121 | 0.3971 | 19.5271 | 0.0274 |
| in_distribution_origin | distance_gated | guidance_margin | 0.7500 | 0.8180 | 0.1820 | 0.3778 | 0.4954 | 20.9675 | 0.0292 |
| in_distribution_origin | distance_gated | guidance_margin | 1.0000 | 0.8440 | 0.1560 | 0.3711 | 0.6429 | 22.9604 | 0.0282 |
| in_distribution_origin | distance_gated | guidance_margin | 1.2500 | 0.8700 | 0.1300 | 0.4854 | 0.8618 | 25.6442 | 0.0291 |
| in_distribution_origin | distance_gated | guidance_margin | 1.5000 | 0.9120 | 0.0880 | 0.5521 | 1.1874 | 29.1919 | 0.0290 |
| in_distribution_origin | distance_gated | guidance_margin | 1.7500 | 0.9480 | 0.0520 | 0.5187 | 1.6762 | 33.8217 | 0.0285 |
| in_distribution_origin | distance_gated | guidance_margin | 2.0000 | 0.9800 | 0.0200 | 0.6033 | 2.4153 | 39.7850 | 0.0288 |
| in_distribution_origin | distance_gated | guidance_margin | 2.5000 | 0.9900 | 0.0100 | 0.5786 | 5.1828 | 56.7460 | 0.0287 |
| ood_shifted_y | baseline | guidance_margin | 0.0000 | 0.7620 | 0.2380 | 0.0767 | 0.2692 | 17.4148 | 0.0228 |
| ood_shifted_y | constant | guidance_margin | 0.0000 | 0.7760 | 0.2240 | 0.2172 | 0.2755 | 17.5063 | 0.0273 |
| ood_shifted_y | constant | guidance_margin | 0.2500 | 0.8200 | 0.1800 | 0.2706 | 0.2853 | 17.6377 | 0.0257 |
| ood_shifted_y | constant | guidance_margin | 0.5000 | 0.8680 | 0.1320 | 0.2982 | 0.3026 | 17.8648 | 0.0264 |
| ood_shifted_y | constant | guidance_margin | 0.7500 | 0.9100 | 0.0900 | 0.3387 | 0.3282 | 18.2041 | 0.0266 |
| ood_shifted_y | constant | guidance_margin | 1.0000 | 0.9500 | 0.0500 | 0.6156 | 0.3616 | 18.6660 | 0.0267 |
| ood_shifted_y | constant | guidance_margin | 1.2500 | 0.9840 | 0.0160 | 0.6031 | 0.4021 | 19.2727 | 0.0262 |
| ood_shifted_y | constant | guidance_margin | 1.5000 | 0.9940 | 0.0060 | 0.8016 | 0.4545 | 20.0903 | 0.0261 |
| ood_shifted_y | constant | guidance_margin | 1.7500 | 1.0000 | 0.0000 | 1.0223 | 0.5239 | 21.1946 | 0.0265 |
| ood_shifted_y | constant | guidance_margin | 2.0000 | 1.0000 | 0.0000 | 1.4181 | 0.6249 | 22.6936 | 0.0269 |
| ood_shifted_y | constant | guidance_margin | 2.5000 | 1.0000 | 0.0000 | 1.2913 | 0.9970 | 27.3816 | 0.0261 |
| ood_shifted_y | distance_gated | guidance_margin | 0.0000 | 0.7760 | 0.2240 | 0.2172 | 0.2755 | 17.5063 | 0.0284 |
| ood_shifted_y | distance_gated | guidance_margin | 0.2500 | 0.8160 | 0.1840 | 0.2788 | 0.2850 | 17.6336 | 0.0297 |
| ood_shifted_y | distance_gated | guidance_margin | 0.5000 | 0.8640 | 0.1360 | 0.2894 | 0.2998 | 17.8253 | 0.0290 |
| ood_shifted_y | distance_gated | guidance_margin | 0.7500 | 0.8980 | 0.1020 | 0.3242 | 0.3197 | 18.0777 | 0.0298 |
| ood_shifted_y | distance_gated | guidance_margin | 1.0000 | 0.9280 | 0.0720 | 0.4883 | 0.3437 | 18.3895 | 0.0287 |
| ood_shifted_y | distance_gated | guidance_margin | 1.2500 | 0.9540 | 0.0460 | 0.6322 | 0.3711 | 18.7675 | 0.0289 |
| ood_shifted_y | distance_gated | guidance_margin | 1.5000 | 0.9880 | 0.0120 | 0.6428 | 0.4022 | 19.2298 | 0.0297 |
| ood_shifted_y | distance_gated | guidance_margin | 1.7500 | 0.9940 | 0.0060 | 0.7768 | 0.4403 | 19.8202 | 0.0288 |
| ood_shifted_y | distance_gated | guidance_margin | 2.0000 | 0.9980 | 0.0020 | 0.4836 | 0.4882 | 20.5759 | 0.0296 |
| ood_shifted_y | distance_gated | guidance_margin | 2.5000 | 1.0000 | 0.0000 | 1.3279 | 0.6305 | 22.7367 | 0.0276 |
| ood_double_gap | baseline | guidance_margin | 0.0000 | 0.5580 | 0.4420 | 0.0609 | 0.2692 | 17.4148 | 0.0222 |
| ood_double_gap | constant | guidance_margin | 0.0000 | 0.5820 | 0.4180 | 0.1619 | 0.2821 | 17.6069 | 0.0284 |
| ood_double_gap | constant | guidance_margin | 0.2500 | 0.6580 | 0.3420 | 0.2792 | 0.3015 | 17.8812 | 0.0273 |
| ood_double_gap | constant | guidance_margin | 0.5000 | 0.7360 | 0.2640 | 0.3935 | 0.3387 | 18.4012 | 0.0288 |
| ood_double_gap | constant | guidance_margin | 0.7500 | 0.8140 | 0.1860 | 0.2662 | 0.4039 | 19.3099 | 0.0287 |
| ood_double_gap | constant | guidance_margin | 1.0000 | 0.8740 | 0.1260 | 0.5538 | 0.5215 | 20.9085 | 0.0296 |
| ood_double_gap | constant | guidance_margin | 1.2500 | 0.9060 | 0.0940 | 0.5171 | 0.7716 | 23.9420 | 0.0282 |
| ood_double_gap | constant | guidance_margin | 1.5000 | 0.9480 | 0.0520 | 0.5363 | 1.3352 | 29.5697 | 0.0288 |
| ood_double_gap | constant | guidance_margin | 1.7500 | 0.9640 | 0.0360 | 0.5660 | 2.6180 | 39.4753 | 0.0289 |
| ood_double_gap | constant | guidance_margin | 2.0000 | 0.9620 | 0.0380 | 0.6463 | 5.4441 | 55.5771 | 0.0291 |
| ood_double_gap | constant | guidance_margin | 2.5000 | 0.9880 | 0.0120 | 0.5917 | 20.4519 | 108.4721 | 0.0284 |
| ood_double_gap | distance_gated | guidance_margin | 0.0000 | 0.5820 | 0.4180 | 0.1619 | 0.2821 | 17.6069 | 0.0329 |
| ood_double_gap | distance_gated | guidance_margin | 0.2500 | 0.6480 | 0.3520 | 0.2757 | 0.3007 | 17.8688 | 0.0327 |
| ood_double_gap | distance_gated | guidance_margin | 0.5000 | 0.7160 | 0.2840 | 0.3812 | 0.3313 | 18.2874 | 0.0330 |
| ood_double_gap | distance_gated | guidance_margin | 0.7500 | 0.7820 | 0.2180 | 0.3713 | 0.3768 | 18.9019 | 0.0330 |
| ood_double_gap | distance_gated | guidance_margin | 1.0000 | 0.8400 | 0.1600 | 0.2868 | 0.4435 | 19.8073 | 0.0330 |
| ood_double_gap | distance_gated | guidance_margin | 1.2500 | 0.8700 | 0.1300 | 0.5830 | 0.5576 | 21.3146 | 0.0322 |
| ood_double_gap | distance_gated | guidance_margin | 1.5000 | 0.9100 | 0.0900 | 0.5057 | 0.7786 | 23.9455 | 0.0328 |
| ood_double_gap | distance_gated | guidance_margin | 1.7500 | 0.9420 | 0.0580 | 0.5017 | 1.2132 | 28.3924 | 0.0330 |
| ood_double_gap | distance_gated | guidance_margin | 2.0000 | 0.9480 | 0.0520 | 0.7318 | 2.0695 | 35.5963 | 0.0319 |
| ood_double_gap | distance_gated | guidance_margin | 2.5000 | 0.9740 | 0.0260 | 0.6643 | 6.7394 | 62.0656 | 0.0327 |
