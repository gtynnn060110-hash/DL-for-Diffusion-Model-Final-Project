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
| in_distribution_origin | conditional | max_guidance_norm | 0.0000 | 0.7220 | 0.2780 | 0.0795 | 0.2885 | 17.8065 | 0.0238 |
| in_distribution_origin | constant | max_guidance_norm | 2.0000 | 0.8380 | 0.1620 | 0.1733 | 1.4866 | 32.8010 | 0.0263 |
| in_distribution_origin | conditional_constant | max_guidance_norm | 2.0000 | 0.8660 | 0.1340 | 0.0841 | 1.6555 | 34.3522 | 0.0267 |
| in_distribution_origin | constant | max_guidance_norm | 2.5000 | 0.8820 | 0.1180 | 0.2614 | 2.1675 | 38.3084 | 0.0263 |
| in_distribution_origin | conditional_constant | max_guidance_norm | 2.5000 | 0.8960 | 0.1040 | 0.2297 | 2.4673 | 40.5233 | 0.0273 |
| in_distribution_origin | constant | max_guidance_norm | 3.0000 | 0.8960 | 0.1040 | 0.4353 | 2.9470 | 43.6878 | 0.0280 |
| in_distribution_origin | conditional_constant | max_guidance_norm | 3.0000 | 0.9260 | 0.0740 | 0.3871 | 3.4021 | 46.5824 | 0.0271 |
| in_distribution_origin | constant | max_guidance_norm | 3.5000 | 0.9180 | 0.0820 | 0.3749 | 3.6958 | 48.3194 | 0.0301 |
| in_distribution_origin | conditional_constant | max_guidance_norm | 3.5000 | 0.9460 | 0.0540 | 0.5298 | 4.3048 | 51.8354 | 0.0294 |
| in_distribution_origin | constant | max_guidance_norm | 4.0000 | 0.9480 | 0.0520 | 0.1082 | 4.3114 | 51.8769 | 0.0280 |
| in_distribution_origin | conditional_constant | max_guidance_norm | 4.0000 | 0.9680 | 0.0320 | 0.6697 | 5.0466 | 55.8820 | 0.0276 |
| in_distribution_origin | constant | max_guidance_norm | 4.5000 | 0.9620 | 0.0380 | 0.2422 | 4.7508 | 54.3135 | 0.0268 |
| in_distribution_origin | conditional_constant | max_guidance_norm | 4.5000 | 0.9740 | 0.0260 | 0.8412 | 5.5758 | 58.6452 | 0.0268 |
| in_distribution_origin | constant | max_guidance_norm | 5.0000 | 0.9700 | 0.0300 | 0.3828 | 5.0290 | 55.8228 | 0.0275 |
| in_distribution_origin | conditional_constant | max_guidance_norm | 5.0000 | 0.9840 | 0.0160 | 0.5139 | 5.9166 | 60.3639 | 0.0264 |
| in_distribution_origin | constant | max_guidance_norm | 6.0000 | 0.9820 | 0.0180 | 0.5920 | 5.2672 | 57.0983 | 0.0270 |
| in_distribution_origin | conditional_constant | max_guidance_norm | 6.0000 | 0.9940 | 0.0060 | 0.5531 | 6.1987 | 61.7675 | 0.0262 |
| in_distribution_origin | constant | max_guidance_norm | 7.0000 | 0.9820 | 0.0180 | 0.6563 | 5.3254 | 57.4076 | 0.0264 |
| in_distribution_origin | conditional_constant | max_guidance_norm | 7.0000 | 0.9920 | 0.0080 | 0.7228 | 6.2615 | 62.0873 | 0.0272 |
| in_distribution_origin | constant | max_guidance_norm | 8.0000 | 0.9820 | 0.0180 | 0.6567 | 5.3360 | 57.4651 | 0.0265 |
| in_distribution_origin | conditional_constant | max_guidance_norm | 8.0000 | 0.9920 | 0.0080 | 0.7398 | 6.2725 | 62.1439 | 0.0254 |
| in_distribution_origin | distance_gated | max_guidance_norm | 2.0000 | 0.8360 | 0.1640 | 0.2510 | 1.0762 | 28.5300 | 0.0284 |
| in_distribution_origin | conditional_distance_gated | max_guidance_norm | 2.0000 | 0.8580 | 0.1420 | 0.1411 | 1.1739 | 29.6352 | 0.0289 |
| in_distribution_origin | distance_gated | max_guidance_norm | 2.5000 | 0.8580 | 0.1420 | 0.1816 | 1.3868 | 31.4805 | 0.0291 |
| in_distribution_origin | conditional_distance_gated | max_guidance_norm | 2.5000 | 0.8720 | 0.1280 | 0.1813 | 1.5187 | 32.7938 | 0.0279 |
| in_distribution_origin | distance_gated | max_guidance_norm | 3.0000 | 0.8840 | 0.1160 | 0.1892 | 1.6772 | 33.9973 | 0.0309 |
| in_distribution_origin | conditional_distance_gated | max_guidance_norm | 3.0000 | 0.9120 | 0.0880 | 0.3361 | 1.8431 | 35.5020 | 0.0302 |
| in_distribution_origin | distance_gated | max_guidance_norm | 3.5000 | 0.9060 | 0.0940 | 0.3182 | 1.9176 | 35.9599 | 0.0286 |
| in_distribution_origin | conditional_distance_gated | max_guidance_norm | 3.5000 | 0.9360 | 0.0640 | 0.4233 | 2.1124 | 37.6245 | 0.0291 |
| in_distribution_origin | distance_gated | max_guidance_norm | 4.0000 | 0.9280 | 0.0720 | 0.2998 | 2.0974 | 37.3735 | 0.0304 |
| in_distribution_origin | conditional_distance_gated | max_guidance_norm | 4.0000 | 0.9500 | 0.0500 | 0.5761 | 2.3146 | 39.1635 | 0.0291 |
| in_distribution_origin | distance_gated | max_guidance_norm | 4.5000 | 0.9500 | 0.0500 | 0.3063 | 2.2246 | 38.3475 | 0.0294 |
| in_distribution_origin | conditional_distance_gated | max_guidance_norm | 4.5000 | 0.9700 | 0.0300 | 0.6996 | 2.4590 | 40.2298 | 0.0288 |
| in_distribution_origin | distance_gated | max_guidance_norm | 5.0000 | 0.9600 | 0.0400 | 0.3765 | 2.3071 | 38.9704 | 0.0297 |
| in_distribution_origin | conditional_distance_gated | max_guidance_norm | 5.0000 | 0.9760 | 0.0240 | 0.7618 | 2.5528 | 40.9117 | 0.0280 |
| in_distribution_origin | distance_gated | max_guidance_norm | 6.0000 | 0.9800 | 0.0200 | 0.5105 | 2.3894 | 39.5839 | 0.0289 |
| in_distribution_origin | conditional_distance_gated | max_guidance_norm | 6.0000 | 0.9820 | 0.0180 | 0.8472 | 2.6447 | 41.5752 | 0.0284 |
| in_distribution_origin | distance_gated | max_guidance_norm | 7.0000 | 0.9800 | 0.0200 | 0.5995 | 2.4116 | 39.7538 | 0.0296 |
| in_distribution_origin | conditional_distance_gated | max_guidance_norm | 7.0000 | 0.9820 | 0.0180 | 0.8534 | 2.6694 | 41.7590 | 0.0300 |
| in_distribution_origin | distance_gated | max_guidance_norm | 8.0000 | 0.9800 | 0.0200 | 0.6033 | 2.4151 | 39.7832 | 0.0294 |
| in_distribution_origin | conditional_distance_gated | max_guidance_norm | 8.0000 | 0.9820 | 0.0180 | 0.8475 | 2.6730 | 41.7891 | 0.0292 |
| ood_shifted_y | baseline | max_guidance_norm | 0.0000 | 0.7620 | 0.2380 | 0.0767 | 0.2692 | 17.4148 | 0.0239 |
| ood_shifted_y | conditional | max_guidance_norm | 0.0000 | 0.8220 | 0.1780 | 0.0570 | 0.2863 | 17.7741 | 0.0227 |
| ood_shifted_y | constant | max_guidance_norm | 2.0000 | 0.9980 | 0.0020 | 0.7941 | 0.4551 | 20.4667 | 0.0270 |
| ood_shifted_y | conditional_constant | max_guidance_norm | 2.0000 | 1.0000 | 0.0000 | 1.2776 | 0.4529 | 20.5514 | 0.0271 |
| ood_shifted_y | constant | max_guidance_norm | 2.5000 | 1.0000 | 0.0000 | 1.0950 | 0.4927 | 20.9983 | 0.0267 |
| ood_shifted_y | conditional_constant | max_guidance_norm | 2.5000 | 1.0000 | 0.0000 | 1.5738 | 0.4889 | 21.0691 | 0.0275 |
| ood_shifted_y | constant | max_guidance_norm | 3.0000 | 1.0000 | 0.0000 | 1.2058 | 0.5255 | 21.4530 | 0.0279 |
| ood_shifted_y | conditional_constant | max_guidance_norm | 3.0000 | 1.0000 | 0.0000 | 1.7517 | 0.5223 | 21.5266 | 0.0272 |
| ood_shifted_y | constant | max_guidance_norm | 3.5000 | 1.0000 | 0.0000 | 1.2267 | 0.5541 | 21.8315 | 0.0275 |
| ood_shifted_y | conditional_constant | max_guidance_norm | 3.5000 | 1.0000 | 0.0000 | 1.8282 | 0.5522 | 21.9161 | 0.0274 |
| ood_shifted_y | constant | max_guidance_norm | 4.0000 | 1.0000 | 0.0000 | 1.2777 | 0.5776 | 22.1297 | 0.0274 |
| ood_shifted_y | conditional_constant | max_guidance_norm | 4.0000 | 1.0000 | 0.0000 | 1.9039 | 0.5773 | 22.2280 | 0.0272 |
| ood_shifted_y | constant | max_guidance_norm | 4.5000 | 1.0000 | 0.0000 | 1.3310 | 0.5956 | 22.3494 | 0.0261 |
| ood_shifted_y | conditional_constant | max_guidance_norm | 4.5000 | 1.0000 | 0.0000 | 1.9191 | 0.5971 | 22.4632 | 0.0274 |
| ood_shifted_y | constant | max_guidance_norm | 5.0000 | 1.0000 | 0.0000 | 1.3867 | 0.6084 | 22.4999 | 0.0269 |
| ood_shifted_y | conditional_constant | max_guidance_norm | 5.0000 | 1.0000 | 0.0000 | 1.9187 | 0.6118 | 22.6310 | 0.0260 |
| ood_shifted_y | constant | max_guidance_norm | 6.0000 | 1.0000 | 0.0000 | 1.4168 | 0.6210 | 22.6468 | 0.0260 |
| ood_shifted_y | conditional_constant | max_guidance_norm | 6.0000 | 1.0000 | 0.0000 | 1.8469 | 0.6269 | 22.7998 | 0.0269 |
| ood_shifted_y | constant | max_guidance_norm | 7.0000 | 1.0000 | 0.0000 | 1.4181 | 0.6243 | 22.6856 | 0.0262 |
| ood_shifted_y | conditional_constant | max_guidance_norm | 7.0000 | 1.0000 | 0.0000 | 1.7652 | 0.6312 | 22.8475 | 0.0264 |
| ood_shifted_y | constant | max_guidance_norm | 8.0000 | 1.0000 | 0.0000 | 1.4181 | 0.6249 | 22.6930 | 0.0261 |
| ood_shifted_y | conditional_constant | max_guidance_norm | 8.0000 | 1.0000 | 0.0000 | 1.7554 | 0.6323 | 22.8584 | 0.0255 |
| ood_shifted_y | distance_gated | max_guidance_norm | 2.0000 | 0.9860 | 0.0140 | 0.5289 | 0.3932 | 19.3687 | 0.0286 |
| ood_shifted_y | conditional_distance_gated | max_guidance_norm | 2.0000 | 0.9940 | 0.0060 | 0.6865 | 0.3937 | 19.5019 | 0.0293 |
| ood_shifted_y | distance_gated | max_guidance_norm | 2.5000 | 0.9940 | 0.0060 | 0.4133 | 0.4157 | 19.6720 | 0.0279 |
| ood_shifted_y | conditional_distance_gated | max_guidance_norm | 2.5000 | 0.9960 | 0.0040 | 0.9404 | 0.4151 | 19.8030 | 0.0291 |
| ood_shifted_y | distance_gated | max_guidance_norm | 3.0000 | 0.9980 | 0.0020 | 0.5043 | 0.4339 | 19.9165 | 0.0278 |
| ood_shifted_y | conditional_distance_gated | max_guidance_norm | 3.0000 | 1.0000 | 0.0000 | 1.0111 | 0.4333 | 20.0536 | 0.0290 |
| ood_shifted_y | distance_gated | max_guidance_norm | 3.5000 | 0.9980 | 0.0020 | 0.6524 | 0.4489 | 20.1100 | 0.0292 |
| ood_shifted_y | conditional_distance_gated | max_guidance_norm | 3.5000 | 1.0000 | 0.0000 | 1.1114 | 0.4485 | 20.2549 | 0.0290 |
| ood_shifted_y | distance_gated | max_guidance_norm | 4.0000 | 0.9960 | 0.0040 | 0.7769 | 0.4613 | 20.2621 | 0.0290 |
| ood_shifted_y | conditional_distance_gated | max_guidance_norm | 4.0000 | 1.0000 | 0.0000 | 1.2204 | 0.4611 | 20.4133 | 0.0354 |
| ood_shifted_y | distance_gated | max_guidance_norm | 4.5000 | 0.9940 | 0.0060 | 0.8814 | 0.4708 | 20.3755 | 0.0312 |
| ood_shifted_y | conditional_distance_gated | max_guidance_norm | 4.5000 | 1.0000 | 0.0000 | 1.3084 | 0.4709 | 20.5329 | 0.0294 |
| ood_shifted_y | distance_gated | max_guidance_norm | 5.0000 | 0.9960 | 0.0040 | 0.6977 | 0.4777 | 20.4554 | 0.0287 |
| ood_shifted_y | conditional_distance_gated | max_guidance_norm | 5.0000 | 1.0000 | 0.0000 | 1.3246 | 0.4780 | 20.6187 | 0.0458 |
| ood_shifted_y | distance_gated | max_guidance_norm | 6.0000 | 0.9960 | 0.0040 | 0.4432 | 0.4854 | 20.5428 | 0.0327 |
| ood_shifted_y | conditional_distance_gated | max_guidance_norm | 6.0000 | 1.0000 | 0.0000 | 1.3259 | 0.4866 | 20.7185 | 0.0303 |
| ood_shifted_y | distance_gated | max_guidance_norm | 7.0000 | 0.9980 | 0.0020 | 0.4556 | 0.4878 | 20.5703 | 0.0289 |
| ood_shifted_y | conditional_distance_gated | max_guidance_norm | 7.0000 | 1.0000 | 0.0000 | 1.3253 | 0.4892 | 20.7501 | 0.0281 |
| ood_shifted_y | distance_gated | max_guidance_norm | 8.0000 | 0.9980 | 0.0020 | 0.4836 | 0.4882 | 20.5755 | 0.0305 |
| ood_shifted_y | conditional_distance_gated | max_guidance_norm | 8.0000 | 1.0000 | 0.0000 | 1.3250 | 0.4897 | 20.7566 | 0.0287 |
| ood_double_gap | baseline | max_guidance_norm | 0.0000 | 0.5580 | 0.4420 | 0.0609 | 0.2692 | 17.4148 | 0.0228 |
| ood_double_gap | conditional | max_guidance_norm | 0.0000 | 0.6900 | 0.3100 | 0.0503 | 0.2915 | 17.9051 | 0.0236 |
| ood_double_gap | constant | max_guidance_norm | 2.0000 | 0.8040 | 0.1960 | 0.1201 | 1.2197 | 29.1206 | 0.0283 |
| ood_double_gap | conditional_constant | max_guidance_norm | 2.0000 | 0.8780 | 0.1220 | 0.3090 | 1.2207 | 29.2709 | 0.0284 |
| ood_double_gap | constant | max_guidance_norm | 2.5000 | 0.8440 | 0.1560 | 0.2430 | 1.8973 | 34.6536 | 0.0293 |
| ood_double_gap | conditional_constant | max_guidance_norm | 2.5000 | 0.9080 | 0.0920 | 0.3060 | 1.8970 | 34.7948 | 0.0283 |
| ood_double_gap | constant | max_guidance_norm | 3.0000 | 0.8860 | 0.1140 | 0.3771 | 2.7950 | 40.7666 | 0.0292 |
| ood_double_gap | conditional_constant | max_guidance_norm | 3.0000 | 0.9220 | 0.0780 | 0.3247 | 2.8126 | 41.0734 | 0.0285 |
| ood_double_gap | constant | max_guidance_norm | 3.5000 | 0.9060 | 0.0940 | 0.3760 | 3.7735 | 46.6046 | 0.0272 |
| ood_double_gap | conditional_constant | max_guidance_norm | 3.5000 | 0.9420 | 0.0580 | 0.3216 | 3.8479 | 47.3042 | 0.0303 |
| ood_double_gap | constant | max_guidance_norm | 4.0000 | 0.9340 | 0.0660 | 0.4410 | 4.6117 | 51.2228 | 0.0292 |
| ood_double_gap | conditional_constant | max_guidance_norm | 4.0000 | 0.9480 | 0.0520 | 0.6121 | 4.7807 | 52.4311 | 0.0287 |
| ood_double_gap | constant | max_guidance_norm | 4.5000 | 0.9480 | 0.0520 | 0.2437 | 5.0452 | 53.5032 | 0.0291 |
| ood_double_gap | conditional_constant | max_guidance_norm | 4.5000 | 0.9440 | 0.0560 | 0.4937 | 5.2693 | 54.9817 | 0.0294 |
| ood_double_gap | constant | max_guidance_norm | 5.0000 | 0.9560 | 0.0440 | 0.3845 | 5.2463 | 54.5538 | 0.0287 |
| ood_double_gap | conditional_constant | max_guidance_norm | 5.0000 | 0.9600 | 0.0400 | 0.4236 | 5.5004 | 56.1628 | 0.0284 |
| ood_double_gap | constant | max_guidance_norm | 6.0000 | 0.9620 | 0.0380 | 0.5628 | 5.3992 | 55.3463 | 0.0290 |
| ood_double_gap | conditional_constant | max_guidance_norm | 6.0000 | 0.9640 | 0.0360 | 0.4205 | 5.6759 | 57.0524 | 0.0286 |
| ood_double_gap | constant | max_guidance_norm | 7.0000 | 0.9620 | 0.0380 | 0.6394 | 5.4356 | 55.5354 | 0.0292 |
| ood_double_gap | conditional_constant | max_guidance_norm | 7.0000 | 0.9640 | 0.0360 | 0.4883 | 5.7158 | 57.2576 | 0.0281 |
| ood_double_gap | constant | max_guidance_norm | 8.0000 | 0.9620 | 0.0380 | 0.6463 | 5.4434 | 55.5743 | 0.0286 |
| ood_double_gap | conditional_constant | max_guidance_norm | 8.0000 | 0.9640 | 0.0360 | 0.5002 | 5.7237 | 57.2993 | 0.0292 |
| ood_double_gap | distance_gated | max_guidance_norm | 2.0000 | 0.7900 | 0.2100 | 0.1916 | 0.9604 | 26.3517 | 0.0328 |
| ood_double_gap | conditional_distance_gated | max_guidance_norm | 2.0000 | 0.8620 | 0.1380 | 0.2803 | 0.9467 | 26.3794 | 0.0335 |
| ood_double_gap | distance_gated | max_guidance_norm | 2.5000 | 0.8100 | 0.1900 | 0.3494 | 1.2839 | 29.3354 | 0.0322 |
| ood_double_gap | conditional_distance_gated | max_guidance_norm | 2.5000 | 0.8880 | 0.1120 | 0.1703 | 1.2540 | 29.2590 | 0.0325 |
| ood_double_gap | distance_gated | max_guidance_norm | 3.0000 | 0.8540 | 0.1460 | 0.2574 | 1.5554 | 31.6137 | 0.0328 |
| ood_double_gap | conditional_distance_gated | max_guidance_norm | 3.0000 | 0.9040 | 0.0960 | 0.3074 | 1.5144 | 31.4963 | 0.0314 |
| ood_double_gap | distance_gated | max_guidance_norm | 3.5000 | 0.8900 | 0.1100 | 0.2850 | 1.7517 | 33.1647 | 0.0324 |
| ood_double_gap | conditional_distance_gated | max_guidance_norm | 3.5000 | 0.9180 | 0.0820 | 0.5244 | 1.7026 | 33.0295 | 0.0317 |
| ood_double_gap | distance_gated | max_guidance_norm | 4.0000 | 0.9200 | 0.0800 | 0.3911 | 1.8808 | 34.1551 | 0.0319 |
| ood_double_gap | conditional_distance_gated | max_guidance_norm | 4.0000 | 0.9340 | 0.0660 | 0.6067 | 1.8313 | 34.0416 | 0.0311 |
| ood_double_gap | distance_gated | max_guidance_norm | 4.5000 | 0.9300 | 0.0700 | 0.5076 | 1.9603 | 34.7605 | 0.0318 |
| ood_double_gap | conditional_distance_gated | max_guidance_norm | 4.5000 | 0.9500 | 0.0500 | 0.4794 | 1.9149 | 34.6846 | 0.0403 |
| ood_double_gap | distance_gated | max_guidance_norm | 5.0000 | 0.9420 | 0.0580 | 0.6100 | 2.0088 | 35.1302 | 0.0744 |
| ood_double_gap | conditional_distance_gated | max_guidance_norm | 5.0000 | 0.9560 | 0.0440 | 0.4443 | 1.9671 | 35.0800 | 0.0523 |
| ood_double_gap | distance_gated | max_guidance_norm | 6.0000 | 0.9520 | 0.0480 | 0.6615 | 2.0542 | 35.4777 | 0.0433 |
| ood_double_gap | conditional_distance_gated | max_guidance_norm | 6.0000 | 0.9780 | 0.0220 | 0.5319 | 2.0178 | 35.4607 | 0.0358 |
| ood_double_gap | distance_gated | max_guidance_norm | 7.0000 | 0.9500 | 0.0500 | 0.7305 | 2.0667 | 35.5750 | 0.0360 |
| ood_double_gap | conditional_distance_gated | max_guidance_norm | 7.0000 | 0.9780 | 0.0220 | 0.5897 | 2.0321 | 35.5704 | 0.0388 |
| ood_double_gap | distance_gated | max_guidance_norm | 8.0000 | 0.9480 | 0.0520 | 0.7318 | 2.0693 | 35.5950 | 0.0395 |
| ood_double_gap | conditional_distance_gated | max_guidance_norm | 8.0000 | 0.9780 | 0.0220 | 0.5804 | 2.0349 | 35.5931 | 0.0362 |

## Scenario Mean Summary

| Scenario | Decay | Param | Value | Success Rate | Collision Rate | Min Distance | Smoothness | Path Length | Time (s) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| in_distribution_origin | baseline | max_guidance_norm | 0.0000 | 0.7280 | 0.2720 | 0.0735 | 0.2692 | 17.4148 | 0.0239 |
| in_distribution_origin | conditional | max_guidance_norm | 0.0000 | 0.7220 | 0.2780 | 0.0795 | 0.2885 | 17.8065 | 0.0238 |
| in_distribution_origin | constant | max_guidance_norm | 2.0000 | 0.8380 | 0.1620 | 0.1733 | 1.4866 | 32.8010 | 0.0263 |
| in_distribution_origin | conditional_constant | max_guidance_norm | 2.0000 | 0.8660 | 0.1340 | 0.0841 | 1.6555 | 34.3522 | 0.0267 |
| in_distribution_origin | constant | max_guidance_norm | 2.5000 | 0.8820 | 0.1180 | 0.2614 | 2.1675 | 38.3084 | 0.0263 |
| in_distribution_origin | conditional_constant | max_guidance_norm | 2.5000 | 0.8960 | 0.1040 | 0.2297 | 2.4673 | 40.5233 | 0.0273 |
| in_distribution_origin | constant | max_guidance_norm | 3.0000 | 0.8960 | 0.1040 | 0.4353 | 2.9470 | 43.6878 | 0.0280 |
| in_distribution_origin | conditional_constant | max_guidance_norm | 3.0000 | 0.9260 | 0.0740 | 0.3871 | 3.4021 | 46.5824 | 0.0271 |
| in_distribution_origin | constant | max_guidance_norm | 3.5000 | 0.9180 | 0.0820 | 0.3749 | 3.6958 | 48.3194 | 0.0301 |
| in_distribution_origin | conditional_constant | max_guidance_norm | 3.5000 | 0.9460 | 0.0540 | 0.5298 | 4.3048 | 51.8354 | 0.0294 |
| in_distribution_origin | constant | max_guidance_norm | 4.0000 | 0.9480 | 0.0520 | 0.1082 | 4.3114 | 51.8769 | 0.0280 |
| in_distribution_origin | conditional_constant | max_guidance_norm | 4.0000 | 0.9680 | 0.0320 | 0.6697 | 5.0466 | 55.8820 | 0.0276 |
| in_distribution_origin | constant | max_guidance_norm | 4.5000 | 0.9620 | 0.0380 | 0.2422 | 4.7508 | 54.3135 | 0.0268 |
| in_distribution_origin | conditional_constant | max_guidance_norm | 4.5000 | 0.9740 | 0.0260 | 0.8412 | 5.5758 | 58.6452 | 0.0268 |
| in_distribution_origin | constant | max_guidance_norm | 5.0000 | 0.9700 | 0.0300 | 0.3828 | 5.0290 | 55.8228 | 0.0275 |
| in_distribution_origin | conditional_constant | max_guidance_norm | 5.0000 | 0.9840 | 0.0160 | 0.5139 | 5.9166 | 60.3639 | 0.0264 |
| in_distribution_origin | constant | max_guidance_norm | 6.0000 | 0.9820 | 0.0180 | 0.5920 | 5.2672 | 57.0983 | 0.0270 |
| in_distribution_origin | conditional_constant | max_guidance_norm | 6.0000 | 0.9940 | 0.0060 | 0.5531 | 6.1987 | 61.7675 | 0.0262 |
| in_distribution_origin | constant | max_guidance_norm | 7.0000 | 0.9820 | 0.0180 | 0.6563 | 5.3254 | 57.4076 | 0.0264 |
| in_distribution_origin | conditional_constant | max_guidance_norm | 7.0000 | 0.9920 | 0.0080 | 0.7228 | 6.2615 | 62.0873 | 0.0272 |
| in_distribution_origin | constant | max_guidance_norm | 8.0000 | 0.9820 | 0.0180 | 0.6567 | 5.3360 | 57.4651 | 0.0265 |
| in_distribution_origin | conditional_constant | max_guidance_norm | 8.0000 | 0.9920 | 0.0080 | 0.7398 | 6.2725 | 62.1439 | 0.0254 |
| in_distribution_origin | distance_gated | max_guidance_norm | 2.0000 | 0.8360 | 0.1640 | 0.2510 | 1.0762 | 28.5300 | 0.0284 |
| in_distribution_origin | conditional_distance_gated | max_guidance_norm | 2.0000 | 0.8580 | 0.1420 | 0.1411 | 1.1739 | 29.6352 | 0.0289 |
| in_distribution_origin | distance_gated | max_guidance_norm | 2.5000 | 0.8580 | 0.1420 | 0.1816 | 1.3868 | 31.4805 | 0.0291 |
| in_distribution_origin | conditional_distance_gated | max_guidance_norm | 2.5000 | 0.8720 | 0.1280 | 0.1813 | 1.5187 | 32.7938 | 0.0279 |
| in_distribution_origin | distance_gated | max_guidance_norm | 3.0000 | 0.8840 | 0.1160 | 0.1892 | 1.6772 | 33.9973 | 0.0309 |
| in_distribution_origin | conditional_distance_gated | max_guidance_norm | 3.0000 | 0.9120 | 0.0880 | 0.3361 | 1.8431 | 35.5020 | 0.0302 |
| in_distribution_origin | distance_gated | max_guidance_norm | 3.5000 | 0.9060 | 0.0940 | 0.3182 | 1.9176 | 35.9599 | 0.0286 |
| in_distribution_origin | conditional_distance_gated | max_guidance_norm | 3.5000 | 0.9360 | 0.0640 | 0.4233 | 2.1124 | 37.6245 | 0.0291 |
| in_distribution_origin | distance_gated | max_guidance_norm | 4.0000 | 0.9280 | 0.0720 | 0.2998 | 2.0974 | 37.3735 | 0.0304 |
| in_distribution_origin | conditional_distance_gated | max_guidance_norm | 4.0000 | 0.9500 | 0.0500 | 0.5761 | 2.3146 | 39.1635 | 0.0291 |
| in_distribution_origin | distance_gated | max_guidance_norm | 4.5000 | 0.9500 | 0.0500 | 0.3063 | 2.2246 | 38.3475 | 0.0294 |
| in_distribution_origin | conditional_distance_gated | max_guidance_norm | 4.5000 | 0.9700 | 0.0300 | 0.6996 | 2.4590 | 40.2298 | 0.0288 |
| in_distribution_origin | distance_gated | max_guidance_norm | 5.0000 | 0.9600 | 0.0400 | 0.3765 | 2.3071 | 38.9704 | 0.0297 |
| in_distribution_origin | conditional_distance_gated | max_guidance_norm | 5.0000 | 0.9760 | 0.0240 | 0.7618 | 2.5528 | 40.9117 | 0.0280 |
| in_distribution_origin | distance_gated | max_guidance_norm | 6.0000 | 0.9800 | 0.0200 | 0.5105 | 2.3894 | 39.5839 | 0.0289 |
| in_distribution_origin | conditional_distance_gated | max_guidance_norm | 6.0000 | 0.9820 | 0.0180 | 0.8472 | 2.6447 | 41.5752 | 0.0284 |
| in_distribution_origin | distance_gated | max_guidance_norm | 7.0000 | 0.9800 | 0.0200 | 0.5995 | 2.4116 | 39.7538 | 0.0296 |
| in_distribution_origin | conditional_distance_gated | max_guidance_norm | 7.0000 | 0.9820 | 0.0180 | 0.8534 | 2.6694 | 41.7590 | 0.0300 |
| in_distribution_origin | distance_gated | max_guidance_norm | 8.0000 | 0.9800 | 0.0200 | 0.6033 | 2.4151 | 39.7832 | 0.0294 |
| in_distribution_origin | conditional_distance_gated | max_guidance_norm | 8.0000 | 0.9820 | 0.0180 | 0.8475 | 2.6730 | 41.7891 | 0.0292 |
| ood_shifted_y | baseline | max_guidance_norm | 0.0000 | 0.7620 | 0.2380 | 0.0767 | 0.2692 | 17.4148 | 0.0239 |
| ood_shifted_y | conditional | max_guidance_norm | 0.0000 | 0.8220 | 0.1780 | 0.0570 | 0.2863 | 17.7741 | 0.0227 |
| ood_shifted_y | constant | max_guidance_norm | 2.0000 | 0.9980 | 0.0020 | 0.7941 | 0.4551 | 20.4667 | 0.0270 |
| ood_shifted_y | conditional_constant | max_guidance_norm | 2.0000 | 1.0000 | 0.0000 | 1.2776 | 0.4529 | 20.5514 | 0.0271 |
| ood_shifted_y | constant | max_guidance_norm | 2.5000 | 1.0000 | 0.0000 | 1.0950 | 0.4927 | 20.9983 | 0.0267 |
| ood_shifted_y | conditional_constant | max_guidance_norm | 2.5000 | 1.0000 | 0.0000 | 1.5738 | 0.4889 | 21.0691 | 0.0275 |
| ood_shifted_y | constant | max_guidance_norm | 3.0000 | 1.0000 | 0.0000 | 1.2058 | 0.5255 | 21.4530 | 0.0279 |
| ood_shifted_y | conditional_constant | max_guidance_norm | 3.0000 | 1.0000 | 0.0000 | 1.7517 | 0.5223 | 21.5266 | 0.0272 |
| ood_shifted_y | constant | max_guidance_norm | 3.5000 | 1.0000 | 0.0000 | 1.2267 | 0.5541 | 21.8315 | 0.0275 |
| ood_shifted_y | conditional_constant | max_guidance_norm | 3.5000 | 1.0000 | 0.0000 | 1.8282 | 0.5522 | 21.9161 | 0.0274 |
| ood_shifted_y | constant | max_guidance_norm | 4.0000 | 1.0000 | 0.0000 | 1.2777 | 0.5776 | 22.1297 | 0.0274 |
| ood_shifted_y | conditional_constant | max_guidance_norm | 4.0000 | 1.0000 | 0.0000 | 1.9039 | 0.5773 | 22.2280 | 0.0272 |
| ood_shifted_y | constant | max_guidance_norm | 4.5000 | 1.0000 | 0.0000 | 1.3310 | 0.5956 | 22.3494 | 0.0261 |
| ood_shifted_y | conditional_constant | max_guidance_norm | 4.5000 | 1.0000 | 0.0000 | 1.9191 | 0.5971 | 22.4632 | 0.0274 |
| ood_shifted_y | constant | max_guidance_norm | 5.0000 | 1.0000 | 0.0000 | 1.3867 | 0.6084 | 22.4999 | 0.0269 |
| ood_shifted_y | conditional_constant | max_guidance_norm | 5.0000 | 1.0000 | 0.0000 | 1.9187 | 0.6118 | 22.6310 | 0.0260 |
| ood_shifted_y | constant | max_guidance_norm | 6.0000 | 1.0000 | 0.0000 | 1.4168 | 0.6210 | 22.6468 | 0.0260 |
| ood_shifted_y | conditional_constant | max_guidance_norm | 6.0000 | 1.0000 | 0.0000 | 1.8469 | 0.6269 | 22.7998 | 0.0269 |
| ood_shifted_y | constant | max_guidance_norm | 7.0000 | 1.0000 | 0.0000 | 1.4181 | 0.6243 | 22.6856 | 0.0262 |
| ood_shifted_y | conditional_constant | max_guidance_norm | 7.0000 | 1.0000 | 0.0000 | 1.7652 | 0.6312 | 22.8475 | 0.0264 |
| ood_shifted_y | constant | max_guidance_norm | 8.0000 | 1.0000 | 0.0000 | 1.4181 | 0.6249 | 22.6930 | 0.0261 |
| ood_shifted_y | conditional_constant | max_guidance_norm | 8.0000 | 1.0000 | 0.0000 | 1.7554 | 0.6323 | 22.8584 | 0.0255 |
| ood_shifted_y | distance_gated | max_guidance_norm | 2.0000 | 0.9860 | 0.0140 | 0.5289 | 0.3932 | 19.3687 | 0.0286 |
| ood_shifted_y | conditional_distance_gated | max_guidance_norm | 2.0000 | 0.9940 | 0.0060 | 0.6865 | 0.3937 | 19.5019 | 0.0293 |
| ood_shifted_y | distance_gated | max_guidance_norm | 2.5000 | 0.9940 | 0.0060 | 0.4133 | 0.4157 | 19.6720 | 0.0279 |
| ood_shifted_y | conditional_distance_gated | max_guidance_norm | 2.5000 | 0.9960 | 0.0040 | 0.9404 | 0.4151 | 19.8030 | 0.0291 |
| ood_shifted_y | distance_gated | max_guidance_norm | 3.0000 | 0.9980 | 0.0020 | 0.5043 | 0.4339 | 19.9165 | 0.0278 |
| ood_shifted_y | conditional_distance_gated | max_guidance_norm | 3.0000 | 1.0000 | 0.0000 | 1.0111 | 0.4333 | 20.0536 | 0.0290 |
| ood_shifted_y | distance_gated | max_guidance_norm | 3.5000 | 0.9980 | 0.0020 | 0.6524 | 0.4489 | 20.1100 | 0.0292 |
| ood_shifted_y | conditional_distance_gated | max_guidance_norm | 3.5000 | 1.0000 | 0.0000 | 1.1114 | 0.4485 | 20.2549 | 0.0290 |
| ood_shifted_y | distance_gated | max_guidance_norm | 4.0000 | 0.9960 | 0.0040 | 0.7769 | 0.4613 | 20.2621 | 0.0290 |
| ood_shifted_y | conditional_distance_gated | max_guidance_norm | 4.0000 | 1.0000 | 0.0000 | 1.2204 | 0.4611 | 20.4133 | 0.0354 |
| ood_shifted_y | distance_gated | max_guidance_norm | 4.5000 | 0.9940 | 0.0060 | 0.8814 | 0.4708 | 20.3755 | 0.0312 |
| ood_shifted_y | conditional_distance_gated | max_guidance_norm | 4.5000 | 1.0000 | 0.0000 | 1.3084 | 0.4709 | 20.5329 | 0.0294 |
| ood_shifted_y | distance_gated | max_guidance_norm | 5.0000 | 0.9960 | 0.0040 | 0.6977 | 0.4777 | 20.4554 | 0.0287 |
| ood_shifted_y | conditional_distance_gated | max_guidance_norm | 5.0000 | 1.0000 | 0.0000 | 1.3246 | 0.4780 | 20.6187 | 0.0458 |
| ood_shifted_y | distance_gated | max_guidance_norm | 6.0000 | 0.9960 | 0.0040 | 0.4432 | 0.4854 | 20.5428 | 0.0327 |
| ood_shifted_y | conditional_distance_gated | max_guidance_norm | 6.0000 | 1.0000 | 0.0000 | 1.3259 | 0.4866 | 20.7185 | 0.0303 |
| ood_shifted_y | distance_gated | max_guidance_norm | 7.0000 | 0.9980 | 0.0020 | 0.4556 | 0.4878 | 20.5703 | 0.0289 |
| ood_shifted_y | conditional_distance_gated | max_guidance_norm | 7.0000 | 1.0000 | 0.0000 | 1.3253 | 0.4892 | 20.7501 | 0.0281 |
| ood_shifted_y | distance_gated | max_guidance_norm | 8.0000 | 0.9980 | 0.0020 | 0.4836 | 0.4882 | 20.5755 | 0.0305 |
| ood_shifted_y | conditional_distance_gated | max_guidance_norm | 8.0000 | 1.0000 | 0.0000 | 1.3250 | 0.4897 | 20.7566 | 0.0287 |
| ood_double_gap | baseline | max_guidance_norm | 0.0000 | 0.5580 | 0.4420 | 0.0609 | 0.2692 | 17.4148 | 0.0228 |
| ood_double_gap | conditional | max_guidance_norm | 0.0000 | 0.6900 | 0.3100 | 0.0503 | 0.2915 | 17.9051 | 0.0236 |
| ood_double_gap | constant | max_guidance_norm | 2.0000 | 0.8040 | 0.1960 | 0.1201 | 1.2197 | 29.1206 | 0.0283 |
| ood_double_gap | conditional_constant | max_guidance_norm | 2.0000 | 0.8780 | 0.1220 | 0.3090 | 1.2207 | 29.2709 | 0.0284 |
| ood_double_gap | constant | max_guidance_norm | 2.5000 | 0.8440 | 0.1560 | 0.2430 | 1.8973 | 34.6536 | 0.0293 |
| ood_double_gap | conditional_constant | max_guidance_norm | 2.5000 | 0.9080 | 0.0920 | 0.3060 | 1.8970 | 34.7948 | 0.0283 |
| ood_double_gap | constant | max_guidance_norm | 3.0000 | 0.8860 | 0.1140 | 0.3771 | 2.7950 | 40.7666 | 0.0292 |
| ood_double_gap | conditional_constant | max_guidance_norm | 3.0000 | 0.9220 | 0.0780 | 0.3247 | 2.8126 | 41.0734 | 0.0285 |
| ood_double_gap | constant | max_guidance_norm | 3.5000 | 0.9060 | 0.0940 | 0.3760 | 3.7735 | 46.6046 | 0.0272 |
| ood_double_gap | conditional_constant | max_guidance_norm | 3.5000 | 0.9420 | 0.0580 | 0.3216 | 3.8479 | 47.3042 | 0.0303 |
| ood_double_gap | constant | max_guidance_norm | 4.0000 | 0.9340 | 0.0660 | 0.4410 | 4.6117 | 51.2228 | 0.0292 |
| ood_double_gap | conditional_constant | max_guidance_norm | 4.0000 | 0.9480 | 0.0520 | 0.6121 | 4.7807 | 52.4311 | 0.0287 |
| ood_double_gap | constant | max_guidance_norm | 4.5000 | 0.9480 | 0.0520 | 0.2437 | 5.0452 | 53.5032 | 0.0291 |
| ood_double_gap | conditional_constant | max_guidance_norm | 4.5000 | 0.9440 | 0.0560 | 0.4937 | 5.2693 | 54.9817 | 0.0294 |
| ood_double_gap | constant | max_guidance_norm | 5.0000 | 0.9560 | 0.0440 | 0.3845 | 5.2463 | 54.5538 | 0.0287 |
| ood_double_gap | conditional_constant | max_guidance_norm | 5.0000 | 0.9600 | 0.0400 | 0.4236 | 5.5004 | 56.1628 | 0.0284 |
| ood_double_gap | constant | max_guidance_norm | 6.0000 | 0.9620 | 0.0380 | 0.5628 | 5.3992 | 55.3463 | 0.0290 |
| ood_double_gap | conditional_constant | max_guidance_norm | 6.0000 | 0.9640 | 0.0360 | 0.4205 | 5.6759 | 57.0524 | 0.0286 |
| ood_double_gap | constant | max_guidance_norm | 7.0000 | 0.9620 | 0.0380 | 0.6394 | 5.4356 | 55.5354 | 0.0292 |
| ood_double_gap | conditional_constant | max_guidance_norm | 7.0000 | 0.9640 | 0.0360 | 0.4883 | 5.7158 | 57.2576 | 0.0281 |
| ood_double_gap | constant | max_guidance_norm | 8.0000 | 0.9620 | 0.0380 | 0.6463 | 5.4434 | 55.5743 | 0.0286 |
| ood_double_gap | conditional_constant | max_guidance_norm | 8.0000 | 0.9640 | 0.0360 | 0.5002 | 5.7237 | 57.2993 | 0.0292 |
| ood_double_gap | distance_gated | max_guidance_norm | 2.0000 | 0.7900 | 0.2100 | 0.1916 | 0.9604 | 26.3517 | 0.0328 |
| ood_double_gap | conditional_distance_gated | max_guidance_norm | 2.0000 | 0.8620 | 0.1380 | 0.2803 | 0.9467 | 26.3794 | 0.0335 |
| ood_double_gap | distance_gated | max_guidance_norm | 2.5000 | 0.8100 | 0.1900 | 0.3494 | 1.2839 | 29.3354 | 0.0322 |
| ood_double_gap | conditional_distance_gated | max_guidance_norm | 2.5000 | 0.8880 | 0.1120 | 0.1703 | 1.2540 | 29.2590 | 0.0325 |
| ood_double_gap | distance_gated | max_guidance_norm | 3.0000 | 0.8540 | 0.1460 | 0.2574 | 1.5554 | 31.6137 | 0.0328 |
| ood_double_gap | conditional_distance_gated | max_guidance_norm | 3.0000 | 0.9040 | 0.0960 | 0.3074 | 1.5144 | 31.4963 | 0.0314 |
| ood_double_gap | distance_gated | max_guidance_norm | 3.5000 | 0.8900 | 0.1100 | 0.2850 | 1.7517 | 33.1647 | 0.0324 |
| ood_double_gap | conditional_distance_gated | max_guidance_norm | 3.5000 | 0.9180 | 0.0820 | 0.5244 | 1.7026 | 33.0295 | 0.0317 |
| ood_double_gap | distance_gated | max_guidance_norm | 4.0000 | 0.9200 | 0.0800 | 0.3911 | 1.8808 | 34.1551 | 0.0319 |
| ood_double_gap | conditional_distance_gated | max_guidance_norm | 4.0000 | 0.9340 | 0.0660 | 0.6067 | 1.8313 | 34.0416 | 0.0311 |
| ood_double_gap | distance_gated | max_guidance_norm | 4.5000 | 0.9300 | 0.0700 | 0.5076 | 1.9603 | 34.7605 | 0.0318 |
| ood_double_gap | conditional_distance_gated | max_guidance_norm | 4.5000 | 0.9500 | 0.0500 | 0.4794 | 1.9149 | 34.6846 | 0.0403 |
| ood_double_gap | distance_gated | max_guidance_norm | 5.0000 | 0.9420 | 0.0580 | 0.6100 | 2.0088 | 35.1302 | 0.0744 |
| ood_double_gap | conditional_distance_gated | max_guidance_norm | 5.0000 | 0.9560 | 0.0440 | 0.4443 | 1.9671 | 35.0800 | 0.0523 |
| ood_double_gap | distance_gated | max_guidance_norm | 6.0000 | 0.9520 | 0.0480 | 0.6615 | 2.0542 | 35.4777 | 0.0433 |
| ood_double_gap | conditional_distance_gated | max_guidance_norm | 6.0000 | 0.9780 | 0.0220 | 0.5319 | 2.0178 | 35.4607 | 0.0358 |
| ood_double_gap | distance_gated | max_guidance_norm | 7.0000 | 0.9500 | 0.0500 | 0.7305 | 2.0667 | 35.5750 | 0.0360 |
| ood_double_gap | conditional_distance_gated | max_guidance_norm | 7.0000 | 0.9780 | 0.0220 | 0.5897 | 2.0321 | 35.5704 | 0.0388 |
| ood_double_gap | distance_gated | max_guidance_norm | 8.0000 | 0.9480 | 0.0520 | 0.7318 | 2.0693 | 35.5950 | 0.0395 |
| ood_double_gap | conditional_distance_gated | max_guidance_norm | 8.0000 | 0.9780 | 0.0220 | 0.5804 | 2.0349 | 35.5931 | 0.0362 |
