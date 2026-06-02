# Guidance Ablation Summary

## Sweep Configuration

- `data_path`: `dataset/toy_trajectories.npy`
- `checkpoint_path`: `checkpoints/rectified_flow_mlp.pt`
- `conditional_checkpoint_path`: `checkpoints/rectified_flow_conditional_mlp.pt`
- `conditional_condition_dim`: `8`
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
| in_distribution_origin | baseline | guidance_margin | 0.0000 | 0.7280 | 0.2720 | 0.0735 | 0.2692 | 17.4148 | 0.0234 |
| in_distribution_origin | conditional | guidance_margin | 0.0000 | 0.7220 | 0.2780 | 0.0795 | 0.2885 | 17.8065 | 0.0222 |
| in_distribution_origin | constant | guidance_margin | 0.0000 | 0.7460 | 0.2540 | 0.2232 | 0.2954 | 17.8878 | 0.0251 |
| in_distribution_origin | conditional_constant | guidance_margin | 0.0000 | 0.7440 | 0.2560 | 0.1919 | 0.3166 | 18.3082 | 0.0259 |
| in_distribution_origin | constant | guidance_margin | 0.2500 | 0.7720 | 0.2280 | 0.3054 | 0.3368 | 18.5920 | 0.0256 |
| in_distribution_origin | conditional_constant | guidance_margin | 0.2500 | 0.7800 | 0.2200 | 0.2915 | 0.3612 | 19.0612 | 0.0252 |
| in_distribution_origin | constant | guidance_margin | 0.5000 | 0.8060 | 0.1940 | 0.4107 | 0.4168 | 19.8624 | 0.0260 |
| in_distribution_origin | conditional_constant | guidance_margin | 0.5000 | 0.8040 | 0.1960 | 0.3448 | 0.4477 | 20.4154 | 0.0250 |
| in_distribution_origin | constant | guidance_margin | 0.7500 | 0.8240 | 0.1760 | 0.2881 | 0.5603 | 21.9359 | 0.0254 |
| in_distribution_origin | conditional_constant | guidance_margin | 0.7500 | 0.8380 | 0.1620 | 0.3931 | 0.6020 | 22.6030 | 0.0265 |
| in_distribution_origin | constant | guidance_margin | 1.0000 | 0.8380 | 0.1620 | 0.3840 | 0.8084 | 25.0986 | 0.0258 |
| in_distribution_origin | conditional_constant | guidance_margin | 1.0000 | 0.8720 | 0.1280 | 0.4587 | 0.8698 | 25.9385 | 0.0251 |
| in_distribution_origin | constant | guidance_margin | 1.2500 | 0.8860 | 0.1140 | 0.4407 | 1.2313 | 29.7149 | 0.0259 |
| in_distribution_origin | conditional_constant | guidance_margin | 1.2500 | 0.9220 | 0.0780 | 0.4451 | 1.3326 | 30.8280 | 0.0237 |
| in_distribution_origin | constant | guidance_margin | 1.5000 | 0.9400 | 0.0600 | 0.3592 | 1.9581 | 36.2675 | 0.0258 |
| in_distribution_origin | conditional_constant | guidance_margin | 1.5000 | 0.9480 | 0.0520 | 0.6455 | 2.1522 | 37.9142 | 0.0268 |
| in_distribution_origin | constant | guidance_margin | 1.7500 | 0.9760 | 0.0240 | 0.4910 | 3.2122 | 45.3236 | 0.0262 |
| in_distribution_origin | conditional_constant | guidance_margin | 1.7500 | 0.9820 | 0.0180 | 0.7338 | 3.6414 | 48.1079 | 0.0258 |
| in_distribution_origin | constant | guidance_margin | 2.0000 | 0.9820 | 0.0180 | 0.6567 | 5.3367 | 57.4689 | 0.0263 |
| in_distribution_origin | conditional_constant | guidance_margin | 2.0000 | 0.9920 | 0.0080 | 0.7398 | 6.2731 | 62.1474 | 0.0245 |
| in_distribution_origin | constant | guidance_margin | 2.5000 | 0.9900 | 0.0100 | 0.8358 | 14.1209 | 92.4387 | 0.0251 |
| in_distribution_origin | conditional_constant | guidance_margin | 2.5000 | 0.9960 | 0.0040 | 0.5388 | 16.7112 | 101.2321 | 0.0259 |
| in_distribution_origin | distance_gated | guidance_margin | 0.0000 | 0.7460 | 0.2540 | 0.2232 | 0.2954 | 17.8878 | 0.0311 |
| in_distribution_origin | conditional_distance_gated | guidance_margin | 0.0000 | 0.7440 | 0.2560 | 0.1919 | 0.3166 | 18.3082 | 0.0272 |
| in_distribution_origin | distance_gated | guidance_margin | 0.2500 | 0.7700 | 0.2300 | 0.3110 | 0.3335 | 18.5293 | 0.0284 |
| in_distribution_origin | conditional_distance_gated | guidance_margin | 0.2500 | 0.7780 | 0.2220 | 0.2917 | 0.3576 | 18.9924 | 0.0281 |
| in_distribution_origin | distance_gated | guidance_margin | 0.5000 | 0.8080 | 0.1920 | 0.4121 | 0.3971 | 19.5271 | 0.0282 |
| in_distribution_origin | conditional_distance_gated | guidance_margin | 0.5000 | 0.7940 | 0.2060 | 0.3373 | 0.4259 | 20.0526 | 0.0281 |
| in_distribution_origin | distance_gated | guidance_margin | 0.7500 | 0.8180 | 0.1820 | 0.3778 | 0.4954 | 20.9675 | 0.0274 |
| in_distribution_origin | conditional_distance_gated | guidance_margin | 0.7500 | 0.8320 | 0.1680 | 0.3935 | 0.5311 | 21.5712 | 0.0268 |
| in_distribution_origin | distance_gated | guidance_margin | 1.0000 | 0.8440 | 0.1560 | 0.3711 | 0.6429 | 22.9604 | 0.0278 |
| in_distribution_origin | conditional_distance_gated | guidance_margin | 1.0000 | 0.8620 | 0.1380 | 0.5466 | 0.6890 | 23.6686 | 0.0276 |
| in_distribution_origin | distance_gated | guidance_margin | 1.2500 | 0.8700 | 0.1300 | 0.4854 | 0.8618 | 25.6442 | 0.0273 |
| in_distribution_origin | conditional_distance_gated | guidance_margin | 1.2500 | 0.9020 | 0.0980 | 0.5226 | 0.9250 | 26.4973 | 0.0277 |
| in_distribution_origin | distance_gated | guidance_margin | 1.5000 | 0.9120 | 0.0880 | 0.5521 | 1.1874 | 29.1919 | 0.0277 |
| in_distribution_origin | conditional_distance_gated | guidance_margin | 1.5000 | 0.9300 | 0.0700 | 0.4845 | 1.2799 | 30.2523 | 0.0295 |
| in_distribution_origin | distance_gated | guidance_margin | 1.7500 | 0.9480 | 0.0520 | 0.5187 | 1.6762 | 33.8217 | 0.0278 |
| in_distribution_origin | conditional_distance_gated | guidance_margin | 1.7500 | 0.9680 | 0.0320 | 0.6852 | 1.8233 | 35.2186 | 0.0266 |
| in_distribution_origin | distance_gated | guidance_margin | 2.0000 | 0.9800 | 0.0200 | 0.6033 | 2.4153 | 39.7850 | 0.0277 |
| in_distribution_origin | conditional_distance_gated | guidance_margin | 2.0000 | 0.9820 | 0.0180 | 0.8475 | 2.6732 | 41.7907 | 0.0280 |
| in_distribution_origin | distance_gated | guidance_margin | 2.5000 | 0.9900 | 0.0100 | 0.5786 | 5.1828 | 56.7460 | 0.0283 |
| in_distribution_origin | conditional_distance_gated | guidance_margin | 2.5000 | 0.9940 | 0.0060 | 0.5631 | 6.0649 | 61.2754 | 0.0272 |
| ood_shifted_y | baseline | guidance_margin | 0.0000 | 0.7620 | 0.2380 | 0.0767 | 0.2692 | 17.4148 | 0.0303 |
| ood_shifted_y | conditional | guidance_margin | 0.0000 | 0.8220 | 0.1780 | 0.0570 | 0.2863 | 17.7741 | 0.0240 |
| ood_shifted_y | constant | guidance_margin | 0.0000 | 0.7760 | 0.2240 | 0.2172 | 0.2755 | 17.5063 | 0.0250 |
| ood_shifted_y | conditional_constant | guidance_margin | 0.0000 | 0.8360 | 0.1640 | 0.3209 | 0.2906 | 17.8319 | 0.0253 |
| ood_shifted_y | constant | guidance_margin | 0.2500 | 0.8200 | 0.1800 | 0.2706 | 0.2853 | 17.6377 | 0.0265 |
| ood_shifted_y | conditional_constant | guidance_margin | 0.2500 | 0.8560 | 0.1440 | 0.4023 | 0.2978 | 17.9251 | 0.0269 |
| ood_shifted_y | constant | guidance_margin | 0.5000 | 0.8680 | 0.1320 | 0.2982 | 0.3026 | 17.8648 | 0.0254 |
| ood_shifted_y | conditional_constant | guidance_margin | 0.5000 | 0.9160 | 0.0840 | 0.4044 | 0.3105 | 18.0913 | 0.0260 |
| ood_shifted_y | constant | guidance_margin | 0.7500 | 0.9100 | 0.0900 | 0.3387 | 0.3282 | 18.2041 | 0.0259 |
| ood_shifted_y | conditional_constant | guidance_margin | 0.7500 | 0.9540 | 0.0460 | 0.5192 | 0.3304 | 18.3635 | 0.0255 |
| ood_shifted_y | constant | guidance_margin | 1.0000 | 0.9500 | 0.0500 | 0.6156 | 0.3616 | 18.6660 | 0.0258 |
| ood_shifted_y | conditional_constant | guidance_margin | 1.0000 | 0.9800 | 0.0200 | 0.6637 | 0.3595 | 18.7877 | 0.0271 |
| ood_shifted_y | constant | guidance_margin | 1.2500 | 0.9840 | 0.0160 | 0.6031 | 0.4021 | 19.2727 | 0.0264 |
| ood_shifted_y | conditional_constant | guidance_margin | 1.2500 | 0.9960 | 0.0040 | 0.8620 | 0.3993 | 19.4000 | 0.0256 |
| ood_shifted_y | constant | guidance_margin | 1.5000 | 0.9940 | 0.0060 | 0.8016 | 0.4545 | 20.0903 | 0.0261 |
| ood_shifted_y | conditional_constant | guidance_margin | 1.5000 | 1.0000 | 0.0000 | 1.1620 | 0.4536 | 20.2464 | 0.0265 |
| ood_shifted_y | constant | guidance_margin | 1.7500 | 1.0000 | 0.0000 | 1.0223 | 0.5239 | 21.1946 | 0.0252 |
| ood_shifted_y | conditional_constant | guidance_margin | 1.7500 | 1.0000 | 0.0000 | 1.3787 | 0.5285 | 21.3730 | 0.0246 |
| ood_shifted_y | constant | guidance_margin | 2.0000 | 1.0000 | 0.0000 | 1.4181 | 0.6249 | 22.6936 | 0.0258 |
| ood_shifted_y | conditional_constant | guidance_margin | 2.0000 | 1.0000 | 0.0000 | 1.7554 | 0.6324 | 22.8594 | 0.0277 |
| ood_shifted_y | constant | guidance_margin | 2.5000 | 1.0000 | 0.0000 | 1.2913 | 0.9970 | 27.3816 | 0.0257 |
| ood_shifted_y | conditional_constant | guidance_margin | 2.5000 | 1.0000 | 0.0000 | 2.1890 | 1.0015 | 27.3174 | 0.0243 |
| ood_shifted_y | distance_gated | guidance_margin | 0.0000 | 0.7760 | 0.2240 | 0.2172 | 0.2755 | 17.5063 | 0.0288 |
| ood_shifted_y | conditional_distance_gated | guidance_margin | 0.0000 | 0.8360 | 0.1640 | 0.3209 | 0.2906 | 17.8319 | 0.0277 |
| ood_shifted_y | distance_gated | guidance_margin | 0.2500 | 0.8160 | 0.1840 | 0.2788 | 0.2850 | 17.6336 | 0.0281 |
| ood_shifted_y | conditional_distance_gated | guidance_margin | 0.2500 | 0.8540 | 0.1460 | 0.4001 | 0.2977 | 17.9243 | 0.0282 |
| ood_shifted_y | distance_gated | guidance_margin | 0.5000 | 0.8640 | 0.1360 | 0.2894 | 0.2998 | 17.8253 | 0.0270 |
| ood_shifted_y | conditional_distance_gated | guidance_margin | 0.5000 | 0.9000 | 0.1000 | 0.4623 | 0.3087 | 18.0668 | 0.0281 |
| ood_shifted_y | distance_gated | guidance_margin | 0.7500 | 0.8980 | 0.1020 | 0.3242 | 0.3197 | 18.0777 | 0.0280 |
| ood_shifted_y | conditional_distance_gated | guidance_margin | 0.7500 | 0.9360 | 0.0640 | 0.4413 | 0.3237 | 18.2615 | 0.0284 |
| ood_shifted_y | distance_gated | guidance_margin | 1.0000 | 0.9280 | 0.0720 | 0.4883 | 0.3437 | 18.3895 | 0.0269 |
| ood_shifted_y | conditional_distance_gated | guidance_margin | 1.0000 | 0.9640 | 0.0360 | 0.6285 | 0.3427 | 18.5245 | 0.0266 |
| ood_shifted_y | distance_gated | guidance_margin | 1.2500 | 0.9540 | 0.0460 | 0.6322 | 0.3711 | 18.7675 | 0.0295 |
| ood_shifted_y | conditional_distance_gated | guidance_margin | 1.2500 | 0.9840 | 0.0160 | 0.7754 | 0.3669 | 18.8775 | 0.0282 |
| ood_shifted_y | distance_gated | guidance_margin | 1.5000 | 0.9880 | 0.0120 | 0.6428 | 0.4022 | 19.2298 | 0.0285 |
| ood_shifted_y | conditional_distance_gated | guidance_margin | 1.5000 | 0.9940 | 0.0060 | 0.9273 | 0.3977 | 19.3479 | 0.0273 |
| ood_shifted_y | distance_gated | guidance_margin | 1.7500 | 0.9940 | 0.0060 | 0.7768 | 0.4403 | 19.8202 | 0.0284 |
| ood_shifted_y | conditional_distance_gated | guidance_margin | 1.7500 | 1.0000 | 0.0000 | 1.1098 | 0.4377 | 19.9709 | 0.0281 |
| ood_shifted_y | distance_gated | guidance_margin | 2.0000 | 0.9980 | 0.0020 | 0.4836 | 0.4882 | 20.5759 | 0.0276 |
| ood_shifted_y | conditional_distance_gated | guidance_margin | 2.0000 | 1.0000 | 0.0000 | 1.3255 | 0.4898 | 20.7573 | 0.0282 |
| ood_shifted_y | distance_gated | guidance_margin | 2.5000 | 1.0000 | 0.0000 | 1.3279 | 0.6305 | 22.7367 | 0.0282 |
| ood_shifted_y | conditional_distance_gated | guidance_margin | 2.5000 | 1.0000 | 0.0000 | 1.3714 | 0.6429 | 22.9439 | 0.0278 |
| ood_double_gap | baseline | guidance_margin | 0.0000 | 0.5580 | 0.4420 | 0.0609 | 0.2692 | 17.4148 | 0.0227 |
| ood_double_gap | conditional | guidance_margin | 0.0000 | 0.6900 | 0.3100 | 0.0503 | 0.2915 | 17.9051 | 0.0238 |
| ood_double_gap | constant | guidance_margin | 0.0000 | 0.5820 | 0.4180 | 0.1619 | 0.2821 | 17.6069 | 0.0279 |
| ood_double_gap | conditional_constant | guidance_margin | 0.0000 | 0.6980 | 0.3020 | 0.2390 | 0.3013 | 18.0396 | 0.0283 |
| ood_double_gap | constant | guidance_margin | 0.2500 | 0.6580 | 0.3420 | 0.2792 | 0.3015 | 17.8812 | 0.0269 |
| ood_double_gap | conditional_constant | guidance_margin | 0.2500 | 0.7620 | 0.2380 | 0.3017 | 0.3169 | 18.2508 | 0.0277 |
| ood_double_gap | constant | guidance_margin | 0.5000 | 0.7360 | 0.2640 | 0.3935 | 0.3387 | 18.4012 | 0.0276 |
| ood_double_gap | conditional_constant | guidance_margin | 0.5000 | 0.8200 | 0.1800 | 0.3782 | 0.3481 | 18.6814 | 0.0274 |
| ood_double_gap | constant | guidance_margin | 0.7500 | 0.8140 | 0.1860 | 0.2662 | 0.4039 | 19.3099 | 0.0284 |
| ood_double_gap | conditional_constant | guidance_margin | 0.7500 | 0.9000 | 0.1000 | 0.5252 | 0.4062 | 19.4938 | 0.0509 |
| ood_double_gap | constant | guidance_margin | 1.0000 | 0.8740 | 0.1260 | 0.5538 | 0.5215 | 20.9085 | 0.0576 |
| ood_double_gap | conditional_constant | guidance_margin | 1.0000 | 0.9240 | 0.0760 | 0.5484 | 0.5174 | 21.0131 | 0.0375 |
| ood_double_gap | constant | guidance_margin | 1.2500 | 0.9060 | 0.0940 | 0.5171 | 0.7716 | 23.9420 | 0.0376 |
| ood_double_gap | conditional_constant | guidance_margin | 1.2500 | 0.9460 | 0.0540 | 0.4757 | 0.7561 | 23.9465 | 0.0309 |
| ood_double_gap | constant | guidance_margin | 1.5000 | 0.9480 | 0.0520 | 0.5363 | 1.3352 | 29.5697 | 0.0271 |
| ood_double_gap | conditional_constant | guidance_margin | 1.5000 | 0.9660 | 0.0340 | 0.5367 | 1.3008 | 29.4668 | 0.0320 |
| ood_double_gap | constant | guidance_margin | 1.7500 | 0.9640 | 0.0360 | 0.5660 | 2.6180 | 39.4753 | 0.0292 |
| ood_double_gap | conditional_constant | guidance_margin | 1.7500 | 0.9740 | 0.0260 | 0.6288 | 2.5996 | 39.6180 | 0.0345 |
| ood_double_gap | constant | guidance_margin | 2.0000 | 0.9620 | 0.0380 | 0.6463 | 5.4441 | 55.5771 | 0.0296 |
| ood_double_gap | conditional_constant | guidance_margin | 2.0000 | 0.9640 | 0.0360 | 0.5002 | 5.7243 | 57.3029 | 0.0307 |
| ood_double_gap | constant | guidance_margin | 2.5000 | 0.9880 | 0.0120 | 0.5917 | 20.4519 | 108.4721 | 0.0330 |
| ood_double_gap | conditional_constant | guidance_margin | 2.5000 | 0.9920 | 0.0080 | 0.9316 | 22.7752 | 115.6753 | 0.0291 |
| ood_double_gap | distance_gated | guidance_margin | 0.0000 | 0.5820 | 0.4180 | 0.1619 | 0.2821 | 17.6069 | 0.0377 |
| ood_double_gap | conditional_distance_gated | guidance_margin | 0.0000 | 0.6980 | 0.3020 | 0.2390 | 0.3013 | 18.0396 | 0.0374 |
| ood_double_gap | distance_gated | guidance_margin | 0.2500 | 0.6480 | 0.3520 | 0.2757 | 0.3007 | 17.8688 | 0.0400 |
| ood_double_gap | conditional_distance_gated | guidance_margin | 0.2500 | 0.7600 | 0.2400 | 0.2976 | 0.3162 | 18.2426 | 0.0341 |
| ood_double_gap | distance_gated | guidance_margin | 0.5000 | 0.7160 | 0.2840 | 0.3812 | 0.3313 | 18.2874 | 0.0325 |
| ood_double_gap | conditional_distance_gated | guidance_margin | 0.5000 | 0.8060 | 0.1940 | 0.3702 | 0.3415 | 18.5856 | 0.0340 |
| ood_double_gap | distance_gated | guidance_margin | 0.7500 | 0.7820 | 0.2180 | 0.3713 | 0.3768 | 18.9019 | 0.0324 |
| ood_double_gap | conditional_distance_gated | guidance_margin | 0.7500 | 0.8740 | 0.1260 | 0.5015 | 0.3805 | 19.1157 | 0.0317 |
| ood_double_gap | distance_gated | guidance_margin | 1.0000 | 0.8400 | 0.1600 | 0.2868 | 0.4435 | 19.8073 | 0.0326 |
| ood_double_gap | conditional_distance_gated | guidance_margin | 1.0000 | 0.9160 | 0.0840 | 0.5468 | 0.4414 | 19.9504 | 0.0319 |
| ood_double_gap | distance_gated | guidance_margin | 1.2500 | 0.8700 | 0.1300 | 0.5830 | 0.5576 | 21.3146 | 0.0316 |
| ood_double_gap | conditional_distance_gated | guidance_margin | 1.2500 | 0.9380 | 0.0620 | 0.4700 | 0.5489 | 21.3865 | 0.0320 |
| ood_double_gap | distance_gated | guidance_margin | 1.5000 | 0.9100 | 0.0900 | 0.5057 | 0.7786 | 23.9455 | 0.0314 |
| ood_double_gap | conditional_distance_gated | guidance_margin | 1.5000 | 0.9620 | 0.0380 | 0.4852 | 0.7581 | 23.9302 | 0.0311 |
| ood_double_gap | distance_gated | guidance_margin | 1.7500 | 0.9420 | 0.0580 | 0.5017 | 1.2132 | 28.3924 | 0.0322 |
| ood_double_gap | conditional_distance_gated | guidance_margin | 1.7500 | 0.9620 | 0.0380 | 0.6716 | 1.1773 | 28.2928 | 0.0307 |
| ood_double_gap | distance_gated | guidance_margin | 2.0000 | 0.9480 | 0.0520 | 0.7318 | 2.0695 | 35.5963 | 0.0323 |
| ood_double_gap | conditional_distance_gated | guidance_margin | 2.0000 | 0.9780 | 0.0220 | 0.5774 | 2.0352 | 35.5953 | 0.0323 |
| ood_double_gap | distance_gated | guidance_margin | 2.5000 | 0.9740 | 0.0260 | 0.6643 | 6.7394 | 62.0656 | 0.0316 |
| ood_double_gap | conditional_distance_gated | guidance_margin | 2.5000 | 0.9780 | 0.0220 | 0.6526 | 7.2880 | 64.8496 | 0.0318 |

## Scenario Mean Summary

| Scenario | Decay | Param | Value | Success Rate | Collision Rate | Min Distance | Smoothness | Path Length | Time (s) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| in_distribution_origin | baseline | guidance_margin | 0.0000 | 0.7280 | 0.2720 | 0.0735 | 0.2692 | 17.4148 | 0.0234 |
| in_distribution_origin | conditional | guidance_margin | 0.0000 | 0.7220 | 0.2780 | 0.0795 | 0.2885 | 17.8065 | 0.0222 |
| in_distribution_origin | constant | guidance_margin | 0.0000 | 0.7460 | 0.2540 | 0.2232 | 0.2954 | 17.8878 | 0.0251 |
| in_distribution_origin | conditional_constant | guidance_margin | 0.0000 | 0.7440 | 0.2560 | 0.1919 | 0.3166 | 18.3082 | 0.0259 |
| in_distribution_origin | constant | guidance_margin | 0.2500 | 0.7720 | 0.2280 | 0.3054 | 0.3368 | 18.5920 | 0.0256 |
| in_distribution_origin | conditional_constant | guidance_margin | 0.2500 | 0.7800 | 0.2200 | 0.2915 | 0.3612 | 19.0612 | 0.0252 |
| in_distribution_origin | constant | guidance_margin | 0.5000 | 0.8060 | 0.1940 | 0.4107 | 0.4168 | 19.8624 | 0.0260 |
| in_distribution_origin | conditional_constant | guidance_margin | 0.5000 | 0.8040 | 0.1960 | 0.3448 | 0.4477 | 20.4154 | 0.0250 |
| in_distribution_origin | constant | guidance_margin | 0.7500 | 0.8240 | 0.1760 | 0.2881 | 0.5603 | 21.9359 | 0.0254 |
| in_distribution_origin | conditional_constant | guidance_margin | 0.7500 | 0.8380 | 0.1620 | 0.3931 | 0.6020 | 22.6030 | 0.0265 |
| in_distribution_origin | constant | guidance_margin | 1.0000 | 0.8380 | 0.1620 | 0.3840 | 0.8084 | 25.0986 | 0.0258 |
| in_distribution_origin | conditional_constant | guidance_margin | 1.0000 | 0.8720 | 0.1280 | 0.4587 | 0.8698 | 25.9385 | 0.0251 |
| in_distribution_origin | constant | guidance_margin | 1.2500 | 0.8860 | 0.1140 | 0.4407 | 1.2313 | 29.7149 | 0.0259 |
| in_distribution_origin | conditional_constant | guidance_margin | 1.2500 | 0.9220 | 0.0780 | 0.4451 | 1.3326 | 30.8280 | 0.0237 |
| in_distribution_origin | constant | guidance_margin | 1.5000 | 0.9400 | 0.0600 | 0.3592 | 1.9581 | 36.2675 | 0.0258 |
| in_distribution_origin | conditional_constant | guidance_margin | 1.5000 | 0.9480 | 0.0520 | 0.6455 | 2.1522 | 37.9142 | 0.0268 |
| in_distribution_origin | constant | guidance_margin | 1.7500 | 0.9760 | 0.0240 | 0.4910 | 3.2122 | 45.3236 | 0.0262 |
| in_distribution_origin | conditional_constant | guidance_margin | 1.7500 | 0.9820 | 0.0180 | 0.7338 | 3.6414 | 48.1079 | 0.0258 |
| in_distribution_origin | constant | guidance_margin | 2.0000 | 0.9820 | 0.0180 | 0.6567 | 5.3367 | 57.4689 | 0.0263 |
| in_distribution_origin | conditional_constant | guidance_margin | 2.0000 | 0.9920 | 0.0080 | 0.7398 | 6.2731 | 62.1474 | 0.0245 |
| in_distribution_origin | constant | guidance_margin | 2.5000 | 0.9900 | 0.0100 | 0.8358 | 14.1209 | 92.4387 | 0.0251 |
| in_distribution_origin | conditional_constant | guidance_margin | 2.5000 | 0.9960 | 0.0040 | 0.5388 | 16.7112 | 101.2321 | 0.0259 |
| in_distribution_origin | distance_gated | guidance_margin | 0.0000 | 0.7460 | 0.2540 | 0.2232 | 0.2954 | 17.8878 | 0.0311 |
| in_distribution_origin | conditional_distance_gated | guidance_margin | 0.0000 | 0.7440 | 0.2560 | 0.1919 | 0.3166 | 18.3082 | 0.0272 |
| in_distribution_origin | distance_gated | guidance_margin | 0.2500 | 0.7700 | 0.2300 | 0.3110 | 0.3335 | 18.5293 | 0.0284 |
| in_distribution_origin | conditional_distance_gated | guidance_margin | 0.2500 | 0.7780 | 0.2220 | 0.2917 | 0.3576 | 18.9924 | 0.0281 |
| in_distribution_origin | distance_gated | guidance_margin | 0.5000 | 0.8080 | 0.1920 | 0.4121 | 0.3971 | 19.5271 | 0.0282 |
| in_distribution_origin | conditional_distance_gated | guidance_margin | 0.5000 | 0.7940 | 0.2060 | 0.3373 | 0.4259 | 20.0526 | 0.0281 |
| in_distribution_origin | distance_gated | guidance_margin | 0.7500 | 0.8180 | 0.1820 | 0.3778 | 0.4954 | 20.9675 | 0.0274 |
| in_distribution_origin | conditional_distance_gated | guidance_margin | 0.7500 | 0.8320 | 0.1680 | 0.3935 | 0.5311 | 21.5712 | 0.0268 |
| in_distribution_origin | distance_gated | guidance_margin | 1.0000 | 0.8440 | 0.1560 | 0.3711 | 0.6429 | 22.9604 | 0.0278 |
| in_distribution_origin | conditional_distance_gated | guidance_margin | 1.0000 | 0.8620 | 0.1380 | 0.5466 | 0.6890 | 23.6686 | 0.0276 |
| in_distribution_origin | distance_gated | guidance_margin | 1.2500 | 0.8700 | 0.1300 | 0.4854 | 0.8618 | 25.6442 | 0.0273 |
| in_distribution_origin | conditional_distance_gated | guidance_margin | 1.2500 | 0.9020 | 0.0980 | 0.5226 | 0.9250 | 26.4973 | 0.0277 |
| in_distribution_origin | distance_gated | guidance_margin | 1.5000 | 0.9120 | 0.0880 | 0.5521 | 1.1874 | 29.1919 | 0.0277 |
| in_distribution_origin | conditional_distance_gated | guidance_margin | 1.5000 | 0.9300 | 0.0700 | 0.4845 | 1.2799 | 30.2523 | 0.0295 |
| in_distribution_origin | distance_gated | guidance_margin | 1.7500 | 0.9480 | 0.0520 | 0.5187 | 1.6762 | 33.8217 | 0.0278 |
| in_distribution_origin | conditional_distance_gated | guidance_margin | 1.7500 | 0.9680 | 0.0320 | 0.6852 | 1.8233 | 35.2186 | 0.0266 |
| in_distribution_origin | distance_gated | guidance_margin | 2.0000 | 0.9800 | 0.0200 | 0.6033 | 2.4153 | 39.7850 | 0.0277 |
| in_distribution_origin | conditional_distance_gated | guidance_margin | 2.0000 | 0.9820 | 0.0180 | 0.8475 | 2.6732 | 41.7907 | 0.0280 |
| in_distribution_origin | distance_gated | guidance_margin | 2.5000 | 0.9900 | 0.0100 | 0.5786 | 5.1828 | 56.7460 | 0.0283 |
| in_distribution_origin | conditional_distance_gated | guidance_margin | 2.5000 | 0.9940 | 0.0060 | 0.5631 | 6.0649 | 61.2754 | 0.0272 |
| ood_shifted_y | baseline | guidance_margin | 0.0000 | 0.7620 | 0.2380 | 0.0767 | 0.2692 | 17.4148 | 0.0303 |
| ood_shifted_y | conditional | guidance_margin | 0.0000 | 0.8220 | 0.1780 | 0.0570 | 0.2863 | 17.7741 | 0.0240 |
| ood_shifted_y | constant | guidance_margin | 0.0000 | 0.7760 | 0.2240 | 0.2172 | 0.2755 | 17.5063 | 0.0250 |
| ood_shifted_y | conditional_constant | guidance_margin | 0.0000 | 0.8360 | 0.1640 | 0.3209 | 0.2906 | 17.8319 | 0.0253 |
| ood_shifted_y | constant | guidance_margin | 0.2500 | 0.8200 | 0.1800 | 0.2706 | 0.2853 | 17.6377 | 0.0265 |
| ood_shifted_y | conditional_constant | guidance_margin | 0.2500 | 0.8560 | 0.1440 | 0.4023 | 0.2978 | 17.9251 | 0.0269 |
| ood_shifted_y | constant | guidance_margin | 0.5000 | 0.8680 | 0.1320 | 0.2982 | 0.3026 | 17.8648 | 0.0254 |
| ood_shifted_y | conditional_constant | guidance_margin | 0.5000 | 0.9160 | 0.0840 | 0.4044 | 0.3105 | 18.0913 | 0.0260 |
| ood_shifted_y | constant | guidance_margin | 0.7500 | 0.9100 | 0.0900 | 0.3387 | 0.3282 | 18.2041 | 0.0259 |
| ood_shifted_y | conditional_constant | guidance_margin | 0.7500 | 0.9540 | 0.0460 | 0.5192 | 0.3304 | 18.3635 | 0.0255 |
| ood_shifted_y | constant | guidance_margin | 1.0000 | 0.9500 | 0.0500 | 0.6156 | 0.3616 | 18.6660 | 0.0258 |
| ood_shifted_y | conditional_constant | guidance_margin | 1.0000 | 0.9800 | 0.0200 | 0.6637 | 0.3595 | 18.7877 | 0.0271 |
| ood_shifted_y | constant | guidance_margin | 1.2500 | 0.9840 | 0.0160 | 0.6031 | 0.4021 | 19.2727 | 0.0264 |
| ood_shifted_y | conditional_constant | guidance_margin | 1.2500 | 0.9960 | 0.0040 | 0.8620 | 0.3993 | 19.4000 | 0.0256 |
| ood_shifted_y | constant | guidance_margin | 1.5000 | 0.9940 | 0.0060 | 0.8016 | 0.4545 | 20.0903 | 0.0261 |
| ood_shifted_y | conditional_constant | guidance_margin | 1.5000 | 1.0000 | 0.0000 | 1.1620 | 0.4536 | 20.2464 | 0.0265 |
| ood_shifted_y | constant | guidance_margin | 1.7500 | 1.0000 | 0.0000 | 1.0223 | 0.5239 | 21.1946 | 0.0252 |
| ood_shifted_y | conditional_constant | guidance_margin | 1.7500 | 1.0000 | 0.0000 | 1.3787 | 0.5285 | 21.3730 | 0.0246 |
| ood_shifted_y | constant | guidance_margin | 2.0000 | 1.0000 | 0.0000 | 1.4181 | 0.6249 | 22.6936 | 0.0258 |
| ood_shifted_y | conditional_constant | guidance_margin | 2.0000 | 1.0000 | 0.0000 | 1.7554 | 0.6324 | 22.8594 | 0.0277 |
| ood_shifted_y | constant | guidance_margin | 2.5000 | 1.0000 | 0.0000 | 1.2913 | 0.9970 | 27.3816 | 0.0257 |
| ood_shifted_y | conditional_constant | guidance_margin | 2.5000 | 1.0000 | 0.0000 | 2.1890 | 1.0015 | 27.3174 | 0.0243 |
| ood_shifted_y | distance_gated | guidance_margin | 0.0000 | 0.7760 | 0.2240 | 0.2172 | 0.2755 | 17.5063 | 0.0288 |
| ood_shifted_y | conditional_distance_gated | guidance_margin | 0.0000 | 0.8360 | 0.1640 | 0.3209 | 0.2906 | 17.8319 | 0.0277 |
| ood_shifted_y | distance_gated | guidance_margin | 0.2500 | 0.8160 | 0.1840 | 0.2788 | 0.2850 | 17.6336 | 0.0281 |
| ood_shifted_y | conditional_distance_gated | guidance_margin | 0.2500 | 0.8540 | 0.1460 | 0.4001 | 0.2977 | 17.9243 | 0.0282 |
| ood_shifted_y | distance_gated | guidance_margin | 0.5000 | 0.8640 | 0.1360 | 0.2894 | 0.2998 | 17.8253 | 0.0270 |
| ood_shifted_y | conditional_distance_gated | guidance_margin | 0.5000 | 0.9000 | 0.1000 | 0.4623 | 0.3087 | 18.0668 | 0.0281 |
| ood_shifted_y | distance_gated | guidance_margin | 0.7500 | 0.8980 | 0.1020 | 0.3242 | 0.3197 | 18.0777 | 0.0280 |
| ood_shifted_y | conditional_distance_gated | guidance_margin | 0.7500 | 0.9360 | 0.0640 | 0.4413 | 0.3237 | 18.2615 | 0.0284 |
| ood_shifted_y | distance_gated | guidance_margin | 1.0000 | 0.9280 | 0.0720 | 0.4883 | 0.3437 | 18.3895 | 0.0269 |
| ood_shifted_y | conditional_distance_gated | guidance_margin | 1.0000 | 0.9640 | 0.0360 | 0.6285 | 0.3427 | 18.5245 | 0.0266 |
| ood_shifted_y | distance_gated | guidance_margin | 1.2500 | 0.9540 | 0.0460 | 0.6322 | 0.3711 | 18.7675 | 0.0295 |
| ood_shifted_y | conditional_distance_gated | guidance_margin | 1.2500 | 0.9840 | 0.0160 | 0.7754 | 0.3669 | 18.8775 | 0.0282 |
| ood_shifted_y | distance_gated | guidance_margin | 1.5000 | 0.9880 | 0.0120 | 0.6428 | 0.4022 | 19.2298 | 0.0285 |
| ood_shifted_y | conditional_distance_gated | guidance_margin | 1.5000 | 0.9940 | 0.0060 | 0.9273 | 0.3977 | 19.3479 | 0.0273 |
| ood_shifted_y | distance_gated | guidance_margin | 1.7500 | 0.9940 | 0.0060 | 0.7768 | 0.4403 | 19.8202 | 0.0284 |
| ood_shifted_y | conditional_distance_gated | guidance_margin | 1.7500 | 1.0000 | 0.0000 | 1.1098 | 0.4377 | 19.9709 | 0.0281 |
| ood_shifted_y | distance_gated | guidance_margin | 2.0000 | 0.9980 | 0.0020 | 0.4836 | 0.4882 | 20.5759 | 0.0276 |
| ood_shifted_y | conditional_distance_gated | guidance_margin | 2.0000 | 1.0000 | 0.0000 | 1.3255 | 0.4898 | 20.7573 | 0.0282 |
| ood_shifted_y | distance_gated | guidance_margin | 2.5000 | 1.0000 | 0.0000 | 1.3279 | 0.6305 | 22.7367 | 0.0282 |
| ood_shifted_y | conditional_distance_gated | guidance_margin | 2.5000 | 1.0000 | 0.0000 | 1.3714 | 0.6429 | 22.9439 | 0.0278 |
| ood_double_gap | baseline | guidance_margin | 0.0000 | 0.5580 | 0.4420 | 0.0609 | 0.2692 | 17.4148 | 0.0227 |
| ood_double_gap | conditional | guidance_margin | 0.0000 | 0.6900 | 0.3100 | 0.0503 | 0.2915 | 17.9051 | 0.0238 |
| ood_double_gap | constant | guidance_margin | 0.0000 | 0.5820 | 0.4180 | 0.1619 | 0.2821 | 17.6069 | 0.0279 |
| ood_double_gap | conditional_constant | guidance_margin | 0.0000 | 0.6980 | 0.3020 | 0.2390 | 0.3013 | 18.0396 | 0.0283 |
| ood_double_gap | constant | guidance_margin | 0.2500 | 0.6580 | 0.3420 | 0.2792 | 0.3015 | 17.8812 | 0.0269 |
| ood_double_gap | conditional_constant | guidance_margin | 0.2500 | 0.7620 | 0.2380 | 0.3017 | 0.3169 | 18.2508 | 0.0277 |
| ood_double_gap | constant | guidance_margin | 0.5000 | 0.7360 | 0.2640 | 0.3935 | 0.3387 | 18.4012 | 0.0276 |
| ood_double_gap | conditional_constant | guidance_margin | 0.5000 | 0.8200 | 0.1800 | 0.3782 | 0.3481 | 18.6814 | 0.0274 |
| ood_double_gap | constant | guidance_margin | 0.7500 | 0.8140 | 0.1860 | 0.2662 | 0.4039 | 19.3099 | 0.0284 |
| ood_double_gap | conditional_constant | guidance_margin | 0.7500 | 0.9000 | 0.1000 | 0.5252 | 0.4062 | 19.4938 | 0.0509 |
| ood_double_gap | constant | guidance_margin | 1.0000 | 0.8740 | 0.1260 | 0.5538 | 0.5215 | 20.9085 | 0.0576 |
| ood_double_gap | conditional_constant | guidance_margin | 1.0000 | 0.9240 | 0.0760 | 0.5484 | 0.5174 | 21.0131 | 0.0375 |
| ood_double_gap | constant | guidance_margin | 1.2500 | 0.9060 | 0.0940 | 0.5171 | 0.7716 | 23.9420 | 0.0376 |
| ood_double_gap | conditional_constant | guidance_margin | 1.2500 | 0.9460 | 0.0540 | 0.4757 | 0.7561 | 23.9465 | 0.0309 |
| ood_double_gap | constant | guidance_margin | 1.5000 | 0.9480 | 0.0520 | 0.5363 | 1.3352 | 29.5697 | 0.0271 |
| ood_double_gap | conditional_constant | guidance_margin | 1.5000 | 0.9660 | 0.0340 | 0.5367 | 1.3008 | 29.4668 | 0.0320 |
| ood_double_gap | constant | guidance_margin | 1.7500 | 0.9640 | 0.0360 | 0.5660 | 2.6180 | 39.4753 | 0.0292 |
| ood_double_gap | conditional_constant | guidance_margin | 1.7500 | 0.9740 | 0.0260 | 0.6288 | 2.5996 | 39.6180 | 0.0345 |
| ood_double_gap | constant | guidance_margin | 2.0000 | 0.9620 | 0.0380 | 0.6463 | 5.4441 | 55.5771 | 0.0296 |
| ood_double_gap | conditional_constant | guidance_margin | 2.0000 | 0.9640 | 0.0360 | 0.5002 | 5.7243 | 57.3029 | 0.0307 |
| ood_double_gap | constant | guidance_margin | 2.5000 | 0.9880 | 0.0120 | 0.5917 | 20.4519 | 108.4721 | 0.0330 |
| ood_double_gap | conditional_constant | guidance_margin | 2.5000 | 0.9920 | 0.0080 | 0.9316 | 22.7752 | 115.6753 | 0.0291 |
| ood_double_gap | distance_gated | guidance_margin | 0.0000 | 0.5820 | 0.4180 | 0.1619 | 0.2821 | 17.6069 | 0.0377 |
| ood_double_gap | conditional_distance_gated | guidance_margin | 0.0000 | 0.6980 | 0.3020 | 0.2390 | 0.3013 | 18.0396 | 0.0374 |
| ood_double_gap | distance_gated | guidance_margin | 0.2500 | 0.6480 | 0.3520 | 0.2757 | 0.3007 | 17.8688 | 0.0400 |
| ood_double_gap | conditional_distance_gated | guidance_margin | 0.2500 | 0.7600 | 0.2400 | 0.2976 | 0.3162 | 18.2426 | 0.0341 |
| ood_double_gap | distance_gated | guidance_margin | 0.5000 | 0.7160 | 0.2840 | 0.3812 | 0.3313 | 18.2874 | 0.0325 |
| ood_double_gap | conditional_distance_gated | guidance_margin | 0.5000 | 0.8060 | 0.1940 | 0.3702 | 0.3415 | 18.5856 | 0.0340 |
| ood_double_gap | distance_gated | guidance_margin | 0.7500 | 0.7820 | 0.2180 | 0.3713 | 0.3768 | 18.9019 | 0.0324 |
| ood_double_gap | conditional_distance_gated | guidance_margin | 0.7500 | 0.8740 | 0.1260 | 0.5015 | 0.3805 | 19.1157 | 0.0317 |
| ood_double_gap | distance_gated | guidance_margin | 1.0000 | 0.8400 | 0.1600 | 0.2868 | 0.4435 | 19.8073 | 0.0326 |
| ood_double_gap | conditional_distance_gated | guidance_margin | 1.0000 | 0.9160 | 0.0840 | 0.5468 | 0.4414 | 19.9504 | 0.0319 |
| ood_double_gap | distance_gated | guidance_margin | 1.2500 | 0.8700 | 0.1300 | 0.5830 | 0.5576 | 21.3146 | 0.0316 |
| ood_double_gap | conditional_distance_gated | guidance_margin | 1.2500 | 0.9380 | 0.0620 | 0.4700 | 0.5489 | 21.3865 | 0.0320 |
| ood_double_gap | distance_gated | guidance_margin | 1.5000 | 0.9100 | 0.0900 | 0.5057 | 0.7786 | 23.9455 | 0.0314 |
| ood_double_gap | conditional_distance_gated | guidance_margin | 1.5000 | 0.9620 | 0.0380 | 0.4852 | 0.7581 | 23.9302 | 0.0311 |
| ood_double_gap | distance_gated | guidance_margin | 1.7500 | 0.9420 | 0.0580 | 0.5017 | 1.2132 | 28.3924 | 0.0322 |
| ood_double_gap | conditional_distance_gated | guidance_margin | 1.7500 | 0.9620 | 0.0380 | 0.6716 | 1.1773 | 28.2928 | 0.0307 |
| ood_double_gap | distance_gated | guidance_margin | 2.0000 | 0.9480 | 0.0520 | 0.7318 | 2.0695 | 35.5963 | 0.0323 |
| ood_double_gap | conditional_distance_gated | guidance_margin | 2.0000 | 0.9780 | 0.0220 | 0.5774 | 2.0352 | 35.5953 | 0.0323 |
| ood_double_gap | distance_gated | guidance_margin | 2.5000 | 0.9740 | 0.0260 | 0.6643 | 6.7394 | 62.0656 | 0.0316 |
| ood_double_gap | conditional_distance_gated | guidance_margin | 2.5000 | 0.9780 | 0.0220 | 0.6526 | 7.2880 | 64.8496 | 0.0318 |
