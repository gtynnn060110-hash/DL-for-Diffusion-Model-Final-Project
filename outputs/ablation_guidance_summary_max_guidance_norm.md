# Guidance Ablation Summary

## Sweep Configuration

- `data_path`: `dataset/toy_trajectories.npy`
- `checkpoint_path`: `checkpoints/rectified_flow_mlp.pt`
- `device`: `cpu`
- `num_samples`: `500`
- `steps`: `20`
- `seed`: `42`
- `ablate`: `max_guidance_norm`
- `values`: `[2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0, 8.0]`
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
| in_distribution_origin | baseline | max_guidance_norm | 0.0000 | 0.7280 | 0.2720 | 0.0735 | 0.2692 | 17.4148 | 0.0239 |
| in_distribution_origin | constant | max_guidance_norm | 2.0000 | 0.8380 | 0.1620 | 0.1733 | 1.4866 | 32.8010 | 0.0260 |
| in_distribution_origin | constant | max_guidance_norm | 2.5000 | 0.8820 | 0.1180 | 0.2614 | 2.1675 | 38.3084 | 0.0249 |
| in_distribution_origin | constant | max_guidance_norm | 3.0000 | 0.8960 | 0.1040 | 0.4353 | 2.9470 | 43.6878 | 0.0261 |
| in_distribution_origin | constant | max_guidance_norm | 3.5000 | 0.9180 | 0.0820 | 0.3749 | 3.6958 | 48.3194 | 0.0269 |
| in_distribution_origin | constant | max_guidance_norm | 4.0000 | 0.9480 | 0.0520 | 0.1082 | 4.3114 | 51.8769 | 0.0259 |
| in_distribution_origin | constant | max_guidance_norm | 4.5000 | 0.9620 | 0.0380 | 0.2422 | 4.7508 | 54.3135 | 0.0271 |
| in_distribution_origin | constant | max_guidance_norm | 5.0000 | 0.9700 | 0.0300 | 0.3828 | 5.0290 | 55.8228 | 0.0260 |
| in_distribution_origin | constant | max_guidance_norm | 6.0000 | 0.9820 | 0.0180 | 0.5920 | 5.2672 | 57.0983 | 0.0258 |
| in_distribution_origin | constant | max_guidance_norm | 7.0000 | 0.9820 | 0.0180 | 0.6563 | 5.3254 | 57.4076 | 0.0267 |
| in_distribution_origin | constant | max_guidance_norm | 8.0000 | 0.9820 | 0.0180 | 0.6567 | 5.3360 | 57.4651 | 0.0337 |
| in_distribution_origin | distance_gated | max_guidance_norm | 2.0000 | 0.8360 | 0.1640 | 0.2510 | 1.0762 | 28.5300 | 0.0289 |
| in_distribution_origin | distance_gated | max_guidance_norm | 2.5000 | 0.8580 | 0.1420 | 0.1816 | 1.3868 | 31.4805 | 0.0290 |
| in_distribution_origin | distance_gated | max_guidance_norm | 3.0000 | 0.8840 | 0.1160 | 0.1892 | 1.6772 | 33.9973 | 0.0287 |
| in_distribution_origin | distance_gated | max_guidance_norm | 3.5000 | 0.9060 | 0.0940 | 0.3182 | 1.9176 | 35.9599 | 0.0296 |
| in_distribution_origin | distance_gated | max_guidance_norm | 4.0000 | 0.9280 | 0.0720 | 0.2998 | 2.0974 | 37.3735 | 0.0288 |
| in_distribution_origin | distance_gated | max_guidance_norm | 4.5000 | 0.9500 | 0.0500 | 0.3063 | 2.2246 | 38.3475 | 0.0281 |
| in_distribution_origin | distance_gated | max_guidance_norm | 5.0000 | 0.9600 | 0.0400 | 0.3765 | 2.3071 | 38.9704 | 0.0286 |
| in_distribution_origin | distance_gated | max_guidance_norm | 6.0000 | 0.9800 | 0.0200 | 0.5105 | 2.3894 | 39.5839 | 0.0282 |
| in_distribution_origin | distance_gated | max_guidance_norm | 7.0000 | 0.9800 | 0.0200 | 0.5995 | 2.4116 | 39.7538 | 0.0375 |
| in_distribution_origin | distance_gated | max_guidance_norm | 8.0000 | 0.9800 | 0.0200 | 0.6033 | 2.4151 | 39.7832 | 0.0288 |
| ood_shifted_y | baseline | max_guidance_norm | 0.0000 | 0.7620 | 0.2380 | 0.0767 | 0.2692 | 17.4148 | 0.0238 |
| ood_shifted_y | constant | max_guidance_norm | 2.0000 | 0.9980 | 0.0020 | 0.7941 | 0.4551 | 20.4667 | 0.0264 |
| ood_shifted_y | constant | max_guidance_norm | 2.5000 | 1.0000 | 0.0000 | 1.0950 | 0.4927 | 20.9983 | 0.0283 |
| ood_shifted_y | constant | max_guidance_norm | 3.0000 | 1.0000 | 0.0000 | 1.2058 | 0.5255 | 21.4530 | 0.0267 |
| ood_shifted_y | constant | max_guidance_norm | 3.5000 | 1.0000 | 0.0000 | 1.2267 | 0.5541 | 21.8315 | 0.0281 |
| ood_shifted_y | constant | max_guidance_norm | 4.0000 | 1.0000 | 0.0000 | 1.2777 | 0.5776 | 22.1297 | 0.0266 |
| ood_shifted_y | constant | max_guidance_norm | 4.5000 | 1.0000 | 0.0000 | 1.3310 | 0.5956 | 22.3494 | 0.0270 |
| ood_shifted_y | constant | max_guidance_norm | 5.0000 | 1.0000 | 0.0000 | 1.3867 | 0.6084 | 22.4999 | 0.0257 |
| ood_shifted_y | constant | max_guidance_norm | 6.0000 | 1.0000 | 0.0000 | 1.4168 | 0.6210 | 22.6468 | 0.0279 |
| ood_shifted_y | constant | max_guidance_norm | 7.0000 | 1.0000 | 0.0000 | 1.4181 | 0.6243 | 22.6856 | 0.0272 |
| ood_shifted_y | constant | max_guidance_norm | 8.0000 | 1.0000 | 0.0000 | 1.4181 | 0.6249 | 22.6930 | 0.0264 |
| ood_shifted_y | distance_gated | max_guidance_norm | 2.0000 | 0.9860 | 0.0140 | 0.5289 | 0.3932 | 19.3687 | 0.0289 |
| ood_shifted_y | distance_gated | max_guidance_norm | 2.5000 | 0.9940 | 0.0060 | 0.4133 | 0.4157 | 19.6720 | 0.0289 |
| ood_shifted_y | distance_gated | max_guidance_norm | 3.0000 | 0.9980 | 0.0020 | 0.5043 | 0.4339 | 19.9165 | 0.0294 |
| ood_shifted_y | distance_gated | max_guidance_norm | 3.5000 | 0.9980 | 0.0020 | 0.6524 | 0.4489 | 20.1100 | 0.0286 |
| ood_shifted_y | distance_gated | max_guidance_norm | 4.0000 | 0.9960 | 0.0040 | 0.7769 | 0.4613 | 20.2621 | 0.0294 |
| ood_shifted_y | distance_gated | max_guidance_norm | 4.5000 | 0.9940 | 0.0060 | 0.8814 | 0.4708 | 20.3755 | 0.0284 |
| ood_shifted_y | distance_gated | max_guidance_norm | 5.0000 | 0.9960 | 0.0040 | 0.6977 | 0.4777 | 20.4554 | 0.0287 |
| ood_shifted_y | distance_gated | max_guidance_norm | 6.0000 | 0.9960 | 0.0040 | 0.4432 | 0.4854 | 20.5428 | 0.0294 |
| ood_shifted_y | distance_gated | max_guidance_norm | 7.0000 | 0.9980 | 0.0020 | 0.4556 | 0.4878 | 20.5703 | 0.0294 |
| ood_shifted_y | distance_gated | max_guidance_norm | 8.0000 | 0.9980 | 0.0020 | 0.4836 | 0.4882 | 20.5755 | 0.0296 |
| ood_double_gap | baseline | max_guidance_norm | 0.0000 | 0.5580 | 0.4420 | 0.0609 | 0.2692 | 17.4148 | 0.0235 |
| ood_double_gap | constant | max_guidance_norm | 2.0000 | 0.8040 | 0.1960 | 0.1201 | 1.2197 | 29.1206 | 0.0295 |
| ood_double_gap | constant | max_guidance_norm | 2.5000 | 0.8440 | 0.1560 | 0.2430 | 1.8973 | 34.6536 | 0.0287 |
| ood_double_gap | constant | max_guidance_norm | 3.0000 | 0.8860 | 0.1140 | 0.3771 | 2.7950 | 40.7666 | 0.0284 |
| ood_double_gap | constant | max_guidance_norm | 3.5000 | 0.9060 | 0.0940 | 0.3760 | 3.7735 | 46.6046 | 0.0288 |
| ood_double_gap | constant | max_guidance_norm | 4.0000 | 0.9340 | 0.0660 | 0.4410 | 4.6117 | 51.2228 | 0.0284 |
| ood_double_gap | constant | max_guidance_norm | 4.5000 | 0.9480 | 0.0520 | 0.2437 | 5.0452 | 53.5032 | 0.0289 |
| ood_double_gap | constant | max_guidance_norm | 5.0000 | 0.9560 | 0.0440 | 0.3845 | 5.2463 | 54.5538 | 0.0291 |
| ood_double_gap | constant | max_guidance_norm | 6.0000 | 0.9620 | 0.0380 | 0.5628 | 5.3992 | 55.3463 | 0.0281 |
| ood_double_gap | constant | max_guidance_norm | 7.0000 | 0.9620 | 0.0380 | 0.6394 | 5.4356 | 55.5354 | 0.0280 |
| ood_double_gap | constant | max_guidance_norm | 8.0000 | 0.9620 | 0.0380 | 0.6463 | 5.4434 | 55.5743 | 0.0284 |
| ood_double_gap | distance_gated | max_guidance_norm | 2.0000 | 0.7900 | 0.2100 | 0.1916 | 0.9604 | 26.3517 | 0.0325 |
| ood_double_gap | distance_gated | max_guidance_norm | 2.5000 | 0.8100 | 0.1900 | 0.3494 | 1.2839 | 29.3354 | 0.0321 |
| ood_double_gap | distance_gated | max_guidance_norm | 3.0000 | 0.8540 | 0.1460 | 0.2574 | 1.5554 | 31.6137 | 0.0325 |
| ood_double_gap | distance_gated | max_guidance_norm | 3.5000 | 0.8900 | 0.1100 | 0.2850 | 1.7517 | 33.1647 | 0.0323 |
| ood_double_gap | distance_gated | max_guidance_norm | 4.0000 | 0.9200 | 0.0800 | 0.3911 | 1.8808 | 34.1551 | 0.0329 |
| ood_double_gap | distance_gated | max_guidance_norm | 4.5000 | 0.9300 | 0.0700 | 0.5076 | 1.9603 | 34.7605 | 0.0333 |
| ood_double_gap | distance_gated | max_guidance_norm | 5.0000 | 0.9420 | 0.0580 | 0.6100 | 2.0088 | 35.1302 | 0.0328 |
| ood_double_gap | distance_gated | max_guidance_norm | 6.0000 | 0.9520 | 0.0480 | 0.6615 | 2.0542 | 35.4777 | 0.0327 |
| ood_double_gap | distance_gated | max_guidance_norm | 7.0000 | 0.9500 | 0.0500 | 0.7305 | 2.0667 | 35.5750 | 0.0331 |
| ood_double_gap | distance_gated | max_guidance_norm | 8.0000 | 0.9480 | 0.0520 | 0.7318 | 2.0693 | 35.5950 | 0.0321 |

## Scenario Mean Summary

| Scenario | Decay | Param | Value | Success Rate | Collision Rate | Min Distance | Smoothness | Path Length | Time (s) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| in_distribution_origin | baseline | max_guidance_norm | 0.0000 | 0.7280 | 0.2720 | 0.0735 | 0.2692 | 17.4148 | 0.0239 |
| in_distribution_origin | constant | max_guidance_norm | 2.0000 | 0.8380 | 0.1620 | 0.1733 | 1.4866 | 32.8010 | 0.0260 |
| in_distribution_origin | constant | max_guidance_norm | 2.5000 | 0.8820 | 0.1180 | 0.2614 | 2.1675 | 38.3084 | 0.0249 |
| in_distribution_origin | constant | max_guidance_norm | 3.0000 | 0.8960 | 0.1040 | 0.4353 | 2.9470 | 43.6878 | 0.0261 |
| in_distribution_origin | constant | max_guidance_norm | 3.5000 | 0.9180 | 0.0820 | 0.3749 | 3.6958 | 48.3194 | 0.0269 |
| in_distribution_origin | constant | max_guidance_norm | 4.0000 | 0.9480 | 0.0520 | 0.1082 | 4.3114 | 51.8769 | 0.0259 |
| in_distribution_origin | constant | max_guidance_norm | 4.5000 | 0.9620 | 0.0380 | 0.2422 | 4.7508 | 54.3135 | 0.0271 |
| in_distribution_origin | constant | max_guidance_norm | 5.0000 | 0.9700 | 0.0300 | 0.3828 | 5.0290 | 55.8228 | 0.0260 |
| in_distribution_origin | constant | max_guidance_norm | 6.0000 | 0.9820 | 0.0180 | 0.5920 | 5.2672 | 57.0983 | 0.0258 |
| in_distribution_origin | constant | max_guidance_norm | 7.0000 | 0.9820 | 0.0180 | 0.6563 | 5.3254 | 57.4076 | 0.0267 |
| in_distribution_origin | constant | max_guidance_norm | 8.0000 | 0.9820 | 0.0180 | 0.6567 | 5.3360 | 57.4651 | 0.0337 |
| in_distribution_origin | distance_gated | max_guidance_norm | 2.0000 | 0.8360 | 0.1640 | 0.2510 | 1.0762 | 28.5300 | 0.0289 |
| in_distribution_origin | distance_gated | max_guidance_norm | 2.5000 | 0.8580 | 0.1420 | 0.1816 | 1.3868 | 31.4805 | 0.0290 |
| in_distribution_origin | distance_gated | max_guidance_norm | 3.0000 | 0.8840 | 0.1160 | 0.1892 | 1.6772 | 33.9973 | 0.0287 |
| in_distribution_origin | distance_gated | max_guidance_norm | 3.5000 | 0.9060 | 0.0940 | 0.3182 | 1.9176 | 35.9599 | 0.0296 |
| in_distribution_origin | distance_gated | max_guidance_norm | 4.0000 | 0.9280 | 0.0720 | 0.2998 | 2.0974 | 37.3735 | 0.0288 |
| in_distribution_origin | distance_gated | max_guidance_norm | 4.5000 | 0.9500 | 0.0500 | 0.3063 | 2.2246 | 38.3475 | 0.0281 |
| in_distribution_origin | distance_gated | max_guidance_norm | 5.0000 | 0.9600 | 0.0400 | 0.3765 | 2.3071 | 38.9704 | 0.0286 |
| in_distribution_origin | distance_gated | max_guidance_norm | 6.0000 | 0.9800 | 0.0200 | 0.5105 | 2.3894 | 39.5839 | 0.0282 |
| in_distribution_origin | distance_gated | max_guidance_norm | 7.0000 | 0.9800 | 0.0200 | 0.5995 | 2.4116 | 39.7538 | 0.0375 |
| in_distribution_origin | distance_gated | max_guidance_norm | 8.0000 | 0.9800 | 0.0200 | 0.6033 | 2.4151 | 39.7832 | 0.0288 |
| ood_shifted_y | baseline | max_guidance_norm | 0.0000 | 0.7620 | 0.2380 | 0.0767 | 0.2692 | 17.4148 | 0.0238 |
| ood_shifted_y | constant | max_guidance_norm | 2.0000 | 0.9980 | 0.0020 | 0.7941 | 0.4551 | 20.4667 | 0.0264 |
| ood_shifted_y | constant | max_guidance_norm | 2.5000 | 1.0000 | 0.0000 | 1.0950 | 0.4927 | 20.9983 | 0.0283 |
| ood_shifted_y | constant | max_guidance_norm | 3.0000 | 1.0000 | 0.0000 | 1.2058 | 0.5255 | 21.4530 | 0.0267 |
| ood_shifted_y | constant | max_guidance_norm | 3.5000 | 1.0000 | 0.0000 | 1.2267 | 0.5541 | 21.8315 | 0.0281 |
| ood_shifted_y | constant | max_guidance_norm | 4.0000 | 1.0000 | 0.0000 | 1.2777 | 0.5776 | 22.1297 | 0.0266 |
| ood_shifted_y | constant | max_guidance_norm | 4.5000 | 1.0000 | 0.0000 | 1.3310 | 0.5956 | 22.3494 | 0.0270 |
| ood_shifted_y | constant | max_guidance_norm | 5.0000 | 1.0000 | 0.0000 | 1.3867 | 0.6084 | 22.4999 | 0.0257 |
| ood_shifted_y | constant | max_guidance_norm | 6.0000 | 1.0000 | 0.0000 | 1.4168 | 0.6210 | 22.6468 | 0.0279 |
| ood_shifted_y | constant | max_guidance_norm | 7.0000 | 1.0000 | 0.0000 | 1.4181 | 0.6243 | 22.6856 | 0.0272 |
| ood_shifted_y | constant | max_guidance_norm | 8.0000 | 1.0000 | 0.0000 | 1.4181 | 0.6249 | 22.6930 | 0.0264 |
| ood_shifted_y | distance_gated | max_guidance_norm | 2.0000 | 0.9860 | 0.0140 | 0.5289 | 0.3932 | 19.3687 | 0.0289 |
| ood_shifted_y | distance_gated | max_guidance_norm | 2.5000 | 0.9940 | 0.0060 | 0.4133 | 0.4157 | 19.6720 | 0.0289 |
| ood_shifted_y | distance_gated | max_guidance_norm | 3.0000 | 0.9980 | 0.0020 | 0.5043 | 0.4339 | 19.9165 | 0.0294 |
| ood_shifted_y | distance_gated | max_guidance_norm | 3.5000 | 0.9980 | 0.0020 | 0.6524 | 0.4489 | 20.1100 | 0.0286 |
| ood_shifted_y | distance_gated | max_guidance_norm | 4.0000 | 0.9960 | 0.0040 | 0.7769 | 0.4613 | 20.2621 | 0.0294 |
| ood_shifted_y | distance_gated | max_guidance_norm | 4.5000 | 0.9940 | 0.0060 | 0.8814 | 0.4708 | 20.3755 | 0.0284 |
| ood_shifted_y | distance_gated | max_guidance_norm | 5.0000 | 0.9960 | 0.0040 | 0.6977 | 0.4777 | 20.4554 | 0.0287 |
| ood_shifted_y | distance_gated | max_guidance_norm | 6.0000 | 0.9960 | 0.0040 | 0.4432 | 0.4854 | 20.5428 | 0.0294 |
| ood_shifted_y | distance_gated | max_guidance_norm | 7.0000 | 0.9980 | 0.0020 | 0.4556 | 0.4878 | 20.5703 | 0.0294 |
| ood_shifted_y | distance_gated | max_guidance_norm | 8.0000 | 0.9980 | 0.0020 | 0.4836 | 0.4882 | 20.5755 | 0.0296 |
| ood_double_gap | baseline | max_guidance_norm | 0.0000 | 0.5580 | 0.4420 | 0.0609 | 0.2692 | 17.4148 | 0.0235 |
| ood_double_gap | constant | max_guidance_norm | 2.0000 | 0.8040 | 0.1960 | 0.1201 | 1.2197 | 29.1206 | 0.0295 |
| ood_double_gap | constant | max_guidance_norm | 2.5000 | 0.8440 | 0.1560 | 0.2430 | 1.8973 | 34.6536 | 0.0287 |
| ood_double_gap | constant | max_guidance_norm | 3.0000 | 0.8860 | 0.1140 | 0.3771 | 2.7950 | 40.7666 | 0.0284 |
| ood_double_gap | constant | max_guidance_norm | 3.5000 | 0.9060 | 0.0940 | 0.3760 | 3.7735 | 46.6046 | 0.0288 |
| ood_double_gap | constant | max_guidance_norm | 4.0000 | 0.9340 | 0.0660 | 0.4410 | 4.6117 | 51.2228 | 0.0284 |
| ood_double_gap | constant | max_guidance_norm | 4.5000 | 0.9480 | 0.0520 | 0.2437 | 5.0452 | 53.5032 | 0.0289 |
| ood_double_gap | constant | max_guidance_norm | 5.0000 | 0.9560 | 0.0440 | 0.3845 | 5.2463 | 54.5538 | 0.0291 |
| ood_double_gap | constant | max_guidance_norm | 6.0000 | 0.9620 | 0.0380 | 0.5628 | 5.3992 | 55.3463 | 0.0281 |
| ood_double_gap | constant | max_guidance_norm | 7.0000 | 0.9620 | 0.0380 | 0.6394 | 5.4356 | 55.5354 | 0.0280 |
| ood_double_gap | constant | max_guidance_norm | 8.0000 | 0.9620 | 0.0380 | 0.6463 | 5.4434 | 55.5743 | 0.0284 |
| ood_double_gap | distance_gated | max_guidance_norm | 2.0000 | 0.7900 | 0.2100 | 0.1916 | 0.9604 | 26.3517 | 0.0325 |
| ood_double_gap | distance_gated | max_guidance_norm | 2.5000 | 0.8100 | 0.1900 | 0.3494 | 1.2839 | 29.3354 | 0.0321 |
| ood_double_gap | distance_gated | max_guidance_norm | 3.0000 | 0.8540 | 0.1460 | 0.2574 | 1.5554 | 31.6137 | 0.0325 |
| ood_double_gap | distance_gated | max_guidance_norm | 3.5000 | 0.8900 | 0.1100 | 0.2850 | 1.7517 | 33.1647 | 0.0323 |
| ood_double_gap | distance_gated | max_guidance_norm | 4.0000 | 0.9200 | 0.0800 | 0.3911 | 1.8808 | 34.1551 | 0.0329 |
| ood_double_gap | distance_gated | max_guidance_norm | 4.5000 | 0.9300 | 0.0700 | 0.5076 | 1.9603 | 34.7605 | 0.0333 |
| ood_double_gap | distance_gated | max_guidance_norm | 5.0000 | 0.9420 | 0.0580 | 0.6100 | 2.0088 | 35.1302 | 0.0328 |
| ood_double_gap | distance_gated | max_guidance_norm | 6.0000 | 0.9520 | 0.0480 | 0.6615 | 2.0542 | 35.4777 | 0.0327 |
| ood_double_gap | distance_gated | max_guidance_norm | 7.0000 | 0.9500 | 0.0500 | 0.7305 | 2.0667 | 35.5750 | 0.0331 |
| ood_double_gap | distance_gated | max_guidance_norm | 8.0000 | 0.9480 | 0.0520 | 0.7318 | 2.0693 | 35.5950 | 0.0321 |
