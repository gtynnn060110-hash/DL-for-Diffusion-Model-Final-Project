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
- `ablate`: `guidance_scale`
- `values`: `[0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]`
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
| in_distribution_origin | baseline | guidance_scale | 0.0000 | 0.7280 | 0.2720 | 0.0735 | 0.2692 | 17.4148 | 0.0223 |
| in_distribution_origin | conditional | guidance_scale | 0.0000 | 0.7220 | 0.2780 | 0.0795 | 0.2885 | 17.8065 | 0.0233 |
| in_distribution_origin | constant | guidance_scale | 0.0000 | 0.7280 | 0.2720 | 0.0735 | 0.2692 | 17.4148 | 0.0257 |
| in_distribution_origin | conditional_constant | guidance_scale | 0.0000 | 0.7220 | 0.2780 | 0.0795 | 0.2885 | 17.8065 | 0.0259 |
| in_distribution_origin | constant | guidance_scale | 0.5000 | 0.8100 | 0.1900 | 0.1677 | 0.4564 | 20.8372 | 0.0254 |
| in_distribution_origin | conditional_constant | guidance_scale | 0.5000 | 0.8080 | 0.1920 | 0.1428 | 0.4933 | 21.4626 | 0.0255 |
| in_distribution_origin | constant | guidance_scale | 1.0000 | 0.8260 | 0.1740 | 0.3039 | 0.8363 | 25.9498 | 0.0299 |
| in_distribution_origin | conditional_constant | guidance_scale | 1.0000 | 0.8500 | 0.1500 | 0.1957 | 0.9090 | 26.8950 | 0.0308 |
| in_distribution_origin | constant | guidance_scale | 1.5000 | 0.8720 | 0.1280 | 0.2939 | 1.4773 | 32.5574 | 0.0252 |
| in_distribution_origin | conditional_constant | guidance_scale | 1.5000 | 0.8960 | 0.1040 | 0.3412 | 1.6315 | 34.0301 | 0.0268 |
| in_distribution_origin | constant | guidance_scale | 2.0000 | 0.9220 | 0.0780 | 0.2746 | 2.4404 | 40.3244 | 0.0253 |
| in_distribution_origin | conditional_constant | guidance_scale | 2.0000 | 0.9540 | 0.0460 | 0.4276 | 2.7641 | 42.6722 | 0.0248 |
| in_distribution_origin | constant | guidance_scale | 2.5000 | 0.9720 | 0.0280 | 0.3913 | 3.7402 | 48.7776 | 0.0251 |
| in_distribution_origin | conditional_constant | guidance_scale | 2.5000 | 0.9800 | 0.0200 | 0.8206 | 4.3411 | 52.3002 | 0.0254 |
| in_distribution_origin | constant | guidance_scale | 3.0000 | 0.9820 | 0.0180 | 0.6567 | 5.3367 | 57.4689 | 0.0251 |
| in_distribution_origin | conditional_constant | guidance_scale | 3.0000 | 0.9920 | 0.0080 | 0.7398 | 6.2731 | 62.1474 | 0.0267 |
| in_distribution_origin | constant | guidance_scale | 4.0000 | 0.9920 | 0.0080 | 0.8411 | 9.0564 | 74.0421 | 0.0255 |
| in_distribution_origin | conditional_constant | guidance_scale | 4.0000 | 0.9980 | 0.0020 | 0.5716 | 10.5488 | 80.1525 | 0.0266 |
| in_distribution_origin | constant | guidance_scale | 5.0000 | 1.0000 | 0.0000 | 1.0180 | 12.7621 | 87.7576 | 0.0249 |
| in_distribution_origin | conditional_constant | guidance_scale | 5.0000 | 0.9980 | 0.0020 | 0.9784 | 14.5232 | 94.2716 | 0.0247 |
| in_distribution_origin | distance_gated | guidance_scale | 0.0000 | 0.7280 | 0.2720 | 0.0735 | 0.2692 | 17.4148 | 0.0261 |
| in_distribution_origin | conditional_distance_gated | guidance_scale | 0.0000 | 0.7220 | 0.2780 | 0.0795 | 0.2885 | 17.8065 | 0.0270 |
| in_distribution_origin | distance_gated | guidance_scale | 0.5000 | 0.8000 | 0.2000 | 0.1625 | 0.3999 | 19.8482 | 0.0258 |
| in_distribution_origin | conditional_distance_gated | guidance_scale | 0.5000 | 0.7960 | 0.2040 | 0.1153 | 0.4313 | 20.4104 | 0.0270 |
| in_distribution_origin | distance_gated | guidance_scale | 1.0000 | 0.8220 | 0.1780 | 0.1167 | 0.6324 | 23.2087 | 0.0273 |
| in_distribution_origin | conditional_distance_gated | guidance_scale | 1.0000 | 0.8460 | 0.1540 | 0.3383 | 0.6831 | 23.9689 | 0.0274 |
| in_distribution_origin | distance_gated | guidance_scale | 1.5000 | 0.8460 | 0.1540 | 0.2489 | 0.9623 | 27.1347 | 0.0277 |
| in_distribution_origin | conditional_distance_gated | guidance_scale | 1.5000 | 0.8800 | 0.1200 | 0.3627 | 1.0426 | 28.1277 | 0.0282 |
| in_distribution_origin | distance_gated | guidance_scale | 2.0000 | 0.9000 | 0.1000 | 0.3563 | 1.3783 | 31.3289 | 0.0272 |
| in_distribution_origin | conditional_distance_gated | guidance_scale | 2.0000 | 0.9340 | 0.0660 | 0.3745 | 1.5026 | 32.6053 | 0.0274 |
| in_distribution_origin | distance_gated | guidance_scale | 2.5000 | 0.9420 | 0.0580 | 0.4250 | 1.8673 | 35.5893 | 0.0268 |
| in_distribution_origin | conditional_distance_gated | guidance_scale | 2.5000 | 0.9620 | 0.0380 | 0.6397 | 2.0505 | 37.2008 | 0.0264 |
| in_distribution_origin | distance_gated | guidance_scale | 3.0000 | 0.9800 | 0.0200 | 0.6033 | 2.4153 | 39.7850 | 0.0272 |
| in_distribution_origin | conditional_distance_gated | guidance_scale | 3.0000 | 0.9820 | 0.0180 | 0.8475 | 2.6732 | 41.7907 | 0.0260 |
| in_distribution_origin | distance_gated | guidance_scale | 4.0000 | 0.9900 | 0.0100 | 0.4468 | 3.6238 | 47.7035 | 0.0268 |
| in_distribution_origin | conditional_distance_gated | guidance_scale | 4.0000 | 0.9940 | 0.0060 | 0.7661 | 4.0701 | 50.5621 | 0.0278 |
| in_distribution_origin | distance_gated | guidance_scale | 5.0000 | 0.9960 | 0.0040 | 0.7809 | 4.8701 | 54.7001 | 0.0270 |
| in_distribution_origin | conditional_distance_gated | guidance_scale | 5.0000 | 0.9960 | 0.0040 | 0.7418 | 5.5147 | 58.3017 | 0.0265 |
| ood_shifted_y | baseline | guidance_scale | 0.0000 | 0.7620 | 0.2380 | 0.0767 | 0.2692 | 17.4148 | 0.0207 |
| ood_shifted_y | conditional | guidance_scale | 0.0000 | 0.8220 | 0.1780 | 0.0570 | 0.2863 | 17.7741 | 0.0215 |
| ood_shifted_y | constant | guidance_scale | 0.0000 | 0.7620 | 0.2380 | 0.0767 | 0.2692 | 17.4148 | 0.0251 |
| ood_shifted_y | conditional_constant | guidance_scale | 0.0000 | 0.8220 | 0.1780 | 0.0570 | 0.2863 | 17.7741 | 0.0254 |
| ood_shifted_y | constant | guidance_scale | 0.5000 | 0.9160 | 0.0840 | 0.1232 | 0.3120 | 18.1545 | 0.0256 |
| ood_shifted_y | conditional_constant | guidance_scale | 0.5000 | 0.9440 | 0.0560 | 0.3288 | 0.3213 | 18.3909 | 0.0250 |
| ood_shifted_y | constant | guidance_scale | 1.0000 | 0.9660 | 0.0340 | 0.2837 | 0.3707 | 19.0707 | 0.0245 |
| ood_shifted_y | conditional_constant | guidance_scale | 1.0000 | 0.9920 | 0.0080 | 0.4842 | 0.3740 | 19.2386 | 0.0256 |
| ood_shifted_y | constant | guidance_scale | 1.5000 | 0.9980 | 0.0020 | 0.5692 | 0.4332 | 20.0194 | 0.0256 |
| ood_shifted_y | conditional_constant | guidance_scale | 1.5000 | 1.0000 | 0.0000 | 1.0773 | 0.4340 | 20.1591 | 0.0251 |
| ood_shifted_y | constant | guidance_scale | 2.0000 | 1.0000 | 0.0000 | 1.0709 | 0.4964 | 20.9451 | 0.0245 |
| ood_shifted_y | conditional_constant | guidance_scale | 2.0000 | 1.0000 | 0.0000 | 1.4623 | 0.4980 | 21.0809 | 0.0246 |
| ood_shifted_y | constant | guidance_scale | 2.5000 | 1.0000 | 0.0000 | 1.1662 | 0.5605 | 21.8376 | 0.0241 |
| ood_shifted_y | conditional_constant | guidance_scale | 2.5000 | 1.0000 | 0.0000 | 1.7547 | 0.5637 | 21.9815 | 0.0246 |
| ood_shifted_y | constant | guidance_scale | 3.0000 | 1.0000 | 0.0000 | 1.4181 | 0.6249 | 22.6936 | 0.0247 |
| ood_shifted_y | conditional_constant | guidance_scale | 3.0000 | 1.0000 | 0.0000 | 1.7554 | 0.6324 | 22.8594 | 0.0249 |
| ood_shifted_y | constant | guidance_scale | 4.0000 | 1.0000 | 0.0000 | 1.6194 | 0.7527 | 24.2692 | 0.0250 |
| ood_shifted_y | conditional_constant | guidance_scale | 4.0000 | 1.0000 | 0.0000 | 1.2036 | 0.7732 | 24.4990 | 0.0253 |
| ood_shifted_y | constant | guidance_scale | 5.0000 | 1.0000 | 0.0000 | 1.6387 | 0.8728 | 25.6210 | 0.0247 |
| ood_shifted_y | conditional_constant | guidance_scale | 5.0000 | 1.0000 | 0.0000 | 1.7055 | 0.9060 | 25.8967 | 0.0252 |
| ood_shifted_y | distance_gated | guidance_scale | 0.0000 | 0.7620 | 0.2380 | 0.0767 | 0.2692 | 17.4148 | 0.0295 |
| ood_shifted_y | conditional_distance_gated | guidance_scale | 0.0000 | 0.8220 | 0.1780 | 0.0570 | 0.2863 | 17.7741 | 0.0270 |
| ood_shifted_y | distance_gated | guidance_scale | 0.5000 | 0.8940 | 0.1060 | 0.2353 | 0.2956 | 17.8406 | 0.0279 |
| ood_shifted_y | conditional_distance_gated | guidance_scale | 0.5000 | 0.9280 | 0.0720 | 0.2884 | 0.3059 | 18.0877 | 0.0276 |
| ood_shifted_y | distance_gated | guidance_scale | 1.0000 | 0.9380 | 0.0620 | 0.4050 | 0.3357 | 18.4296 | 0.0269 |
| ood_shifted_y | conditional_distance_gated | guidance_scale | 1.0000 | 0.9680 | 0.0320 | 0.3250 | 0.3398 | 18.6052 | 0.0286 |
| ood_shifted_y | distance_gated | guidance_scale | 1.5000 | 0.9720 | 0.0280 | 0.3500 | 0.3768 | 19.0229 | 0.0278 |
| ood_shifted_y | conditional_distance_gated | guidance_scale | 1.5000 | 0.9900 | 0.0100 | 0.6919 | 0.3772 | 19.1698 | 0.0276 |
| ood_shifted_y | distance_gated | guidance_scale | 2.0000 | 0.9900 | 0.0100 | 0.5884 | 0.4161 | 19.5821 | 0.0272 |
| ood_shifted_y | conditional_distance_gated | guidance_scale | 2.0000 | 0.9980 | 0.0020 | 0.9615 | 0.4151 | 19.7303 | 0.0274 |
| ood_shifted_y | distance_gated | guidance_scale | 2.5000 | 0.9960 | 0.0040 | 0.7441 | 0.4533 | 20.0997 | 0.0280 |
| ood_shifted_y | conditional_distance_gated | guidance_scale | 2.5000 | 1.0000 | 0.0000 | 1.1618 | 0.4528 | 20.2626 | 0.0284 |
| ood_shifted_y | distance_gated | guidance_scale | 3.0000 | 0.9980 | 0.0020 | 0.4836 | 0.4882 | 20.5759 | 0.0276 |
| ood_shifted_y | conditional_distance_gated | guidance_scale | 3.0000 | 1.0000 | 0.0000 | 1.3255 | 0.4898 | 20.7573 | 0.0286 |
| ood_shifted_y | distance_gated | guidance_scale | 4.0000 | 0.9980 | 0.0020 | 0.9639 | 0.5490 | 21.4027 | 0.0275 |
| ood_shifted_y | conditional_distance_gated | guidance_scale | 4.0000 | 1.0000 | 0.0000 | 1.3064 | 0.5581 | 21.6336 | 0.0291 |
| ood_shifted_y | distance_gated | guidance_scale | 5.0000 | 1.0000 | 0.0000 | 1.2500 | 0.6015 | 22.0902 | 0.0282 |
| ood_shifted_y | conditional_distance_gated | guidance_scale | 5.0000 | 1.0000 | 0.0000 | 1.6355 | 0.6177 | 22.3682 | 0.0287 |
| ood_double_gap | baseline | guidance_scale | 0.0000 | 0.5580 | 0.4420 | 0.0609 | 0.2692 | 17.4148 | 0.0221 |
| ood_double_gap | conditional | guidance_scale | 0.0000 | 0.6900 | 0.3100 | 0.0503 | 0.2915 | 17.9051 | 0.0225 |
| ood_double_gap | constant | guidance_scale | 0.0000 | 0.5580 | 0.4420 | 0.0609 | 0.2692 | 17.4148 | 0.0275 |
| ood_double_gap | conditional_constant | guidance_scale | 0.0000 | 0.6900 | 0.3100 | 0.0503 | 0.2915 | 17.9051 | 0.0281 |
| ood_double_gap | constant | guidance_scale | 0.5000 | 0.6900 | 0.3100 | 0.1623 | 0.3853 | 19.4416 | 0.0283 |
| ood_double_gap | conditional_constant | guidance_scale | 0.5000 | 0.7920 | 0.2080 | 0.1748 | 0.4024 | 19.8154 | 0.0278 |
| ood_double_gap | constant | guidance_scale | 1.0000 | 0.7700 | 0.2300 | 0.2169 | 0.6606 | 23.1349 | 0.0276 |
| ood_double_gap | conditional_constant | guidance_scale | 1.0000 | 0.8400 | 0.1600 | 0.2411 | 0.6635 | 23.3291 | 0.0272 |
| ood_double_gap | constant | guidance_scale | 1.5000 | 0.8240 | 0.1760 | 0.3185 | 1.1894 | 28.6431 | 0.0277 |
| ood_double_gap | conditional_constant | guidance_scale | 1.5000 | 0.8880 | 0.1120 | 0.3879 | 1.1734 | 28.6841 | 0.0275 |
| ood_double_gap | constant | guidance_scale | 2.0000 | 0.9060 | 0.0940 | 0.3796 | 2.0981 | 36.0621 | 0.0273 |
| ood_double_gap | conditional_constant | guidance_scale | 2.0000 | 0.9220 | 0.0780 | 0.6422 | 2.0814 | 36.1662 | 0.0271 |
| ood_double_gap | constant | guidance_scale | 2.5000 | 0.9400 | 0.0600 | 0.6782 | 3.5037 | 45.1970 | 0.0279 |
| ood_double_gap | conditional_constant | guidance_scale | 2.5000 | 0.9500 | 0.0500 | 0.4427 | 3.5678 | 45.8824 | 0.0278 |
| ood_double_gap | constant | guidance_scale | 3.0000 | 0.9620 | 0.0380 | 0.6463 | 5.4441 | 55.5771 | 0.0280 |
| ood_double_gap | conditional_constant | guidance_scale | 3.0000 | 0.9640 | 0.0360 | 0.5002 | 5.7243 | 57.3029 | 0.0282 |
| ood_double_gap | constant | guidance_scale | 4.0000 | 0.9920 | 0.0080 | 0.8026 | 10.5147 | 77.1415 | 0.0276 |
| ood_double_gap | conditional_constant | guidance_scale | 4.0000 | 0.9860 | 0.0140 | 0.8661 | 11.4997 | 81.1638 | 0.0279 |
| ood_double_gap | constant | guidance_scale | 5.0000 | 0.9980 | 0.0020 | 0.9281 | 15.8535 | 95.5107 | 0.0284 |
| ood_double_gap | conditional_constant | guidance_scale | 5.0000 | 1.0000 | 0.0000 | 1.1181 | 17.3012 | 100.5029 | 0.0276 |
| ood_double_gap | distance_gated | guidance_scale | 0.0000 | 0.5580 | 0.4420 | 0.0609 | 0.2692 | 17.4148 | 0.0307 |
| ood_double_gap | conditional_distance_gated | guidance_scale | 0.0000 | 0.6900 | 0.3100 | 0.0503 | 0.2915 | 17.9051 | 0.0312 |
| ood_double_gap | distance_gated | guidance_scale | 0.5000 | 0.6780 | 0.3220 | 0.1497 | 0.3449 | 18.7421 | 0.0314 |
| ood_double_gap | conditional_distance_gated | guidance_scale | 0.5000 | 0.7780 | 0.2220 | 0.1714 | 0.3613 | 19.1067 | 0.0320 |
| ood_double_gap | distance_gated | guidance_scale | 1.0000 | 0.7440 | 0.2560 | 0.2519 | 0.5004 | 20.9544 | 0.0315 |
| ood_double_gap | conditional_distance_gated | guidance_scale | 1.0000 | 0.8340 | 0.1660 | 0.3048 | 0.5046 | 21.1592 | 0.0313 |
| ood_double_gap | distance_gated | guidance_scale | 1.5000 | 0.8100 | 0.1900 | 0.3188 | 0.7427 | 23.8579 | 0.0318 |
| ood_double_gap | conditional_distance_gated | guidance_scale | 1.5000 | 0.8720 | 0.1280 | 0.3358 | 0.7312 | 23.9139 | 0.0398 |
| ood_double_gap | distance_gated | guidance_scale | 2.0000 | 0.8540 | 0.1460 | 0.4992 | 1.0793 | 27.3239 | 0.0298 |
| ood_double_gap | conditional_distance_gated | guidance_scale | 2.0000 | 0.9140 | 0.0860 | 0.5683 | 1.0517 | 27.2729 | 0.0310 |
| ood_double_gap | distance_gated | guidance_scale | 2.5000 | 0.9160 | 0.0840 | 0.5931 | 1.5196 | 31.2680 | 0.0309 |
| ood_double_gap | conditional_distance_gated | guidance_scale | 2.5000 | 0.9420 | 0.0580 | 0.7311 | 1.4815 | 31.1848 | 0.0309 |
| ood_double_gap | distance_gated | guidance_scale | 3.0000 | 0.9480 | 0.0520 | 0.7318 | 2.0695 | 35.5963 | 0.0312 |
| ood_double_gap | conditional_distance_gated | guidance_scale | 3.0000 | 0.9780 | 0.0220 | 0.5774 | 2.0352 | 35.5953 | 0.0365 |
| ood_double_gap | distance_gated | guidance_scale | 4.0000 | 0.9800 | 0.0200 | 0.7718 | 3.4750 | 44.9015 | 0.0325 |
| ood_double_gap | conditional_distance_gated | guidance_scale | 4.0000 | 0.9820 | 0.0180 | 0.6724 | 3.5176 | 45.4724 | 0.0315 |
| ood_double_gap | distance_gated | guidance_scale | 5.0000 | 0.9940 | 0.0060 | 0.8918 | 5.1720 | 54.2869 | 0.0323 |
| ood_double_gap | conditional_distance_gated | guidance_scale | 5.0000 | 0.9940 | 0.0060 | 0.6586 | 5.4113 | 55.8220 | 0.0324 |

## Scenario Mean Summary

| Scenario | Decay | Param | Value | Success Rate | Collision Rate | Min Distance | Smoothness | Path Length | Time (s) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| in_distribution_origin | baseline | guidance_scale | 0.0000 | 0.7280 | 0.2720 | 0.0735 | 0.2692 | 17.4148 | 0.0223 |
| in_distribution_origin | conditional | guidance_scale | 0.0000 | 0.7220 | 0.2780 | 0.0795 | 0.2885 | 17.8065 | 0.0233 |
| in_distribution_origin | constant | guidance_scale | 0.0000 | 0.7280 | 0.2720 | 0.0735 | 0.2692 | 17.4148 | 0.0257 |
| in_distribution_origin | conditional_constant | guidance_scale | 0.0000 | 0.7220 | 0.2780 | 0.0795 | 0.2885 | 17.8065 | 0.0259 |
| in_distribution_origin | constant | guidance_scale | 0.5000 | 0.8100 | 0.1900 | 0.1677 | 0.4564 | 20.8372 | 0.0254 |
| in_distribution_origin | conditional_constant | guidance_scale | 0.5000 | 0.8080 | 0.1920 | 0.1428 | 0.4933 | 21.4626 | 0.0255 |
| in_distribution_origin | constant | guidance_scale | 1.0000 | 0.8260 | 0.1740 | 0.3039 | 0.8363 | 25.9498 | 0.0299 |
| in_distribution_origin | conditional_constant | guidance_scale | 1.0000 | 0.8500 | 0.1500 | 0.1957 | 0.9090 | 26.8950 | 0.0308 |
| in_distribution_origin | constant | guidance_scale | 1.5000 | 0.8720 | 0.1280 | 0.2939 | 1.4773 | 32.5574 | 0.0252 |
| in_distribution_origin | conditional_constant | guidance_scale | 1.5000 | 0.8960 | 0.1040 | 0.3412 | 1.6315 | 34.0301 | 0.0268 |
| in_distribution_origin | constant | guidance_scale | 2.0000 | 0.9220 | 0.0780 | 0.2746 | 2.4404 | 40.3244 | 0.0253 |
| in_distribution_origin | conditional_constant | guidance_scale | 2.0000 | 0.9540 | 0.0460 | 0.4276 | 2.7641 | 42.6722 | 0.0248 |
| in_distribution_origin | constant | guidance_scale | 2.5000 | 0.9720 | 0.0280 | 0.3913 | 3.7402 | 48.7776 | 0.0251 |
| in_distribution_origin | conditional_constant | guidance_scale | 2.5000 | 0.9800 | 0.0200 | 0.8206 | 4.3411 | 52.3002 | 0.0254 |
| in_distribution_origin | constant | guidance_scale | 3.0000 | 0.9820 | 0.0180 | 0.6567 | 5.3367 | 57.4689 | 0.0251 |
| in_distribution_origin | conditional_constant | guidance_scale | 3.0000 | 0.9920 | 0.0080 | 0.7398 | 6.2731 | 62.1474 | 0.0267 |
| in_distribution_origin | constant | guidance_scale | 4.0000 | 0.9920 | 0.0080 | 0.8411 | 9.0564 | 74.0421 | 0.0255 |
| in_distribution_origin | conditional_constant | guidance_scale | 4.0000 | 0.9980 | 0.0020 | 0.5716 | 10.5488 | 80.1525 | 0.0266 |
| in_distribution_origin | constant | guidance_scale | 5.0000 | 1.0000 | 0.0000 | 1.0180 | 12.7621 | 87.7576 | 0.0249 |
| in_distribution_origin | conditional_constant | guidance_scale | 5.0000 | 0.9980 | 0.0020 | 0.9784 | 14.5232 | 94.2716 | 0.0247 |
| in_distribution_origin | distance_gated | guidance_scale | 0.0000 | 0.7280 | 0.2720 | 0.0735 | 0.2692 | 17.4148 | 0.0261 |
| in_distribution_origin | conditional_distance_gated | guidance_scale | 0.0000 | 0.7220 | 0.2780 | 0.0795 | 0.2885 | 17.8065 | 0.0270 |
| in_distribution_origin | distance_gated | guidance_scale | 0.5000 | 0.8000 | 0.2000 | 0.1625 | 0.3999 | 19.8482 | 0.0258 |
| in_distribution_origin | conditional_distance_gated | guidance_scale | 0.5000 | 0.7960 | 0.2040 | 0.1153 | 0.4313 | 20.4104 | 0.0270 |
| in_distribution_origin | distance_gated | guidance_scale | 1.0000 | 0.8220 | 0.1780 | 0.1167 | 0.6324 | 23.2087 | 0.0273 |
| in_distribution_origin | conditional_distance_gated | guidance_scale | 1.0000 | 0.8460 | 0.1540 | 0.3383 | 0.6831 | 23.9689 | 0.0274 |
| in_distribution_origin | distance_gated | guidance_scale | 1.5000 | 0.8460 | 0.1540 | 0.2489 | 0.9623 | 27.1347 | 0.0277 |
| in_distribution_origin | conditional_distance_gated | guidance_scale | 1.5000 | 0.8800 | 0.1200 | 0.3627 | 1.0426 | 28.1277 | 0.0282 |
| in_distribution_origin | distance_gated | guidance_scale | 2.0000 | 0.9000 | 0.1000 | 0.3563 | 1.3783 | 31.3289 | 0.0272 |
| in_distribution_origin | conditional_distance_gated | guidance_scale | 2.0000 | 0.9340 | 0.0660 | 0.3745 | 1.5026 | 32.6053 | 0.0274 |
| in_distribution_origin | distance_gated | guidance_scale | 2.5000 | 0.9420 | 0.0580 | 0.4250 | 1.8673 | 35.5893 | 0.0268 |
| in_distribution_origin | conditional_distance_gated | guidance_scale | 2.5000 | 0.9620 | 0.0380 | 0.6397 | 2.0505 | 37.2008 | 0.0264 |
| in_distribution_origin | distance_gated | guidance_scale | 3.0000 | 0.9800 | 0.0200 | 0.6033 | 2.4153 | 39.7850 | 0.0272 |
| in_distribution_origin | conditional_distance_gated | guidance_scale | 3.0000 | 0.9820 | 0.0180 | 0.8475 | 2.6732 | 41.7907 | 0.0260 |
| in_distribution_origin | distance_gated | guidance_scale | 4.0000 | 0.9900 | 0.0100 | 0.4468 | 3.6238 | 47.7035 | 0.0268 |
| in_distribution_origin | conditional_distance_gated | guidance_scale | 4.0000 | 0.9940 | 0.0060 | 0.7661 | 4.0701 | 50.5621 | 0.0278 |
| in_distribution_origin | distance_gated | guidance_scale | 5.0000 | 0.9960 | 0.0040 | 0.7809 | 4.8701 | 54.7001 | 0.0270 |
| in_distribution_origin | conditional_distance_gated | guidance_scale | 5.0000 | 0.9960 | 0.0040 | 0.7418 | 5.5147 | 58.3017 | 0.0265 |
| ood_shifted_y | baseline | guidance_scale | 0.0000 | 0.7620 | 0.2380 | 0.0767 | 0.2692 | 17.4148 | 0.0207 |
| ood_shifted_y | conditional | guidance_scale | 0.0000 | 0.8220 | 0.1780 | 0.0570 | 0.2863 | 17.7741 | 0.0215 |
| ood_shifted_y | constant | guidance_scale | 0.0000 | 0.7620 | 0.2380 | 0.0767 | 0.2692 | 17.4148 | 0.0251 |
| ood_shifted_y | conditional_constant | guidance_scale | 0.0000 | 0.8220 | 0.1780 | 0.0570 | 0.2863 | 17.7741 | 0.0254 |
| ood_shifted_y | constant | guidance_scale | 0.5000 | 0.9160 | 0.0840 | 0.1232 | 0.3120 | 18.1545 | 0.0256 |
| ood_shifted_y | conditional_constant | guidance_scale | 0.5000 | 0.9440 | 0.0560 | 0.3288 | 0.3213 | 18.3909 | 0.0250 |
| ood_shifted_y | constant | guidance_scale | 1.0000 | 0.9660 | 0.0340 | 0.2837 | 0.3707 | 19.0707 | 0.0245 |
| ood_shifted_y | conditional_constant | guidance_scale | 1.0000 | 0.9920 | 0.0080 | 0.4842 | 0.3740 | 19.2386 | 0.0256 |
| ood_shifted_y | constant | guidance_scale | 1.5000 | 0.9980 | 0.0020 | 0.5692 | 0.4332 | 20.0194 | 0.0256 |
| ood_shifted_y | conditional_constant | guidance_scale | 1.5000 | 1.0000 | 0.0000 | 1.0773 | 0.4340 | 20.1591 | 0.0251 |
| ood_shifted_y | constant | guidance_scale | 2.0000 | 1.0000 | 0.0000 | 1.0709 | 0.4964 | 20.9451 | 0.0245 |
| ood_shifted_y | conditional_constant | guidance_scale | 2.0000 | 1.0000 | 0.0000 | 1.4623 | 0.4980 | 21.0809 | 0.0246 |
| ood_shifted_y | constant | guidance_scale | 2.5000 | 1.0000 | 0.0000 | 1.1662 | 0.5605 | 21.8376 | 0.0241 |
| ood_shifted_y | conditional_constant | guidance_scale | 2.5000 | 1.0000 | 0.0000 | 1.7547 | 0.5637 | 21.9815 | 0.0246 |
| ood_shifted_y | constant | guidance_scale | 3.0000 | 1.0000 | 0.0000 | 1.4181 | 0.6249 | 22.6936 | 0.0247 |
| ood_shifted_y | conditional_constant | guidance_scale | 3.0000 | 1.0000 | 0.0000 | 1.7554 | 0.6324 | 22.8594 | 0.0249 |
| ood_shifted_y | constant | guidance_scale | 4.0000 | 1.0000 | 0.0000 | 1.6194 | 0.7527 | 24.2692 | 0.0250 |
| ood_shifted_y | conditional_constant | guidance_scale | 4.0000 | 1.0000 | 0.0000 | 1.2036 | 0.7732 | 24.4990 | 0.0253 |
| ood_shifted_y | constant | guidance_scale | 5.0000 | 1.0000 | 0.0000 | 1.6387 | 0.8728 | 25.6210 | 0.0247 |
| ood_shifted_y | conditional_constant | guidance_scale | 5.0000 | 1.0000 | 0.0000 | 1.7055 | 0.9060 | 25.8967 | 0.0252 |
| ood_shifted_y | distance_gated | guidance_scale | 0.0000 | 0.7620 | 0.2380 | 0.0767 | 0.2692 | 17.4148 | 0.0295 |
| ood_shifted_y | conditional_distance_gated | guidance_scale | 0.0000 | 0.8220 | 0.1780 | 0.0570 | 0.2863 | 17.7741 | 0.0270 |
| ood_shifted_y | distance_gated | guidance_scale | 0.5000 | 0.8940 | 0.1060 | 0.2353 | 0.2956 | 17.8406 | 0.0279 |
| ood_shifted_y | conditional_distance_gated | guidance_scale | 0.5000 | 0.9280 | 0.0720 | 0.2884 | 0.3059 | 18.0877 | 0.0276 |
| ood_shifted_y | distance_gated | guidance_scale | 1.0000 | 0.9380 | 0.0620 | 0.4050 | 0.3357 | 18.4296 | 0.0269 |
| ood_shifted_y | conditional_distance_gated | guidance_scale | 1.0000 | 0.9680 | 0.0320 | 0.3250 | 0.3398 | 18.6052 | 0.0286 |
| ood_shifted_y | distance_gated | guidance_scale | 1.5000 | 0.9720 | 0.0280 | 0.3500 | 0.3768 | 19.0229 | 0.0278 |
| ood_shifted_y | conditional_distance_gated | guidance_scale | 1.5000 | 0.9900 | 0.0100 | 0.6919 | 0.3772 | 19.1698 | 0.0276 |
| ood_shifted_y | distance_gated | guidance_scale | 2.0000 | 0.9900 | 0.0100 | 0.5884 | 0.4161 | 19.5821 | 0.0272 |
| ood_shifted_y | conditional_distance_gated | guidance_scale | 2.0000 | 0.9980 | 0.0020 | 0.9615 | 0.4151 | 19.7303 | 0.0274 |
| ood_shifted_y | distance_gated | guidance_scale | 2.5000 | 0.9960 | 0.0040 | 0.7441 | 0.4533 | 20.0997 | 0.0280 |
| ood_shifted_y | conditional_distance_gated | guidance_scale | 2.5000 | 1.0000 | 0.0000 | 1.1618 | 0.4528 | 20.2626 | 0.0284 |
| ood_shifted_y | distance_gated | guidance_scale | 3.0000 | 0.9980 | 0.0020 | 0.4836 | 0.4882 | 20.5759 | 0.0276 |
| ood_shifted_y | conditional_distance_gated | guidance_scale | 3.0000 | 1.0000 | 0.0000 | 1.3255 | 0.4898 | 20.7573 | 0.0286 |
| ood_shifted_y | distance_gated | guidance_scale | 4.0000 | 0.9980 | 0.0020 | 0.9639 | 0.5490 | 21.4027 | 0.0275 |
| ood_shifted_y | conditional_distance_gated | guidance_scale | 4.0000 | 1.0000 | 0.0000 | 1.3064 | 0.5581 | 21.6336 | 0.0291 |
| ood_shifted_y | distance_gated | guidance_scale | 5.0000 | 1.0000 | 0.0000 | 1.2500 | 0.6015 | 22.0902 | 0.0282 |
| ood_shifted_y | conditional_distance_gated | guidance_scale | 5.0000 | 1.0000 | 0.0000 | 1.6355 | 0.6177 | 22.3682 | 0.0287 |
| ood_double_gap | baseline | guidance_scale | 0.0000 | 0.5580 | 0.4420 | 0.0609 | 0.2692 | 17.4148 | 0.0221 |
| ood_double_gap | conditional | guidance_scale | 0.0000 | 0.6900 | 0.3100 | 0.0503 | 0.2915 | 17.9051 | 0.0225 |
| ood_double_gap | constant | guidance_scale | 0.0000 | 0.5580 | 0.4420 | 0.0609 | 0.2692 | 17.4148 | 0.0275 |
| ood_double_gap | conditional_constant | guidance_scale | 0.0000 | 0.6900 | 0.3100 | 0.0503 | 0.2915 | 17.9051 | 0.0281 |
| ood_double_gap | constant | guidance_scale | 0.5000 | 0.6900 | 0.3100 | 0.1623 | 0.3853 | 19.4416 | 0.0283 |
| ood_double_gap | conditional_constant | guidance_scale | 0.5000 | 0.7920 | 0.2080 | 0.1748 | 0.4024 | 19.8154 | 0.0278 |
| ood_double_gap | constant | guidance_scale | 1.0000 | 0.7700 | 0.2300 | 0.2169 | 0.6606 | 23.1349 | 0.0276 |
| ood_double_gap | conditional_constant | guidance_scale | 1.0000 | 0.8400 | 0.1600 | 0.2411 | 0.6635 | 23.3291 | 0.0272 |
| ood_double_gap | constant | guidance_scale | 1.5000 | 0.8240 | 0.1760 | 0.3185 | 1.1894 | 28.6431 | 0.0277 |
| ood_double_gap | conditional_constant | guidance_scale | 1.5000 | 0.8880 | 0.1120 | 0.3879 | 1.1734 | 28.6841 | 0.0275 |
| ood_double_gap | constant | guidance_scale | 2.0000 | 0.9060 | 0.0940 | 0.3796 | 2.0981 | 36.0621 | 0.0273 |
| ood_double_gap | conditional_constant | guidance_scale | 2.0000 | 0.9220 | 0.0780 | 0.6422 | 2.0814 | 36.1662 | 0.0271 |
| ood_double_gap | constant | guidance_scale | 2.5000 | 0.9400 | 0.0600 | 0.6782 | 3.5037 | 45.1970 | 0.0279 |
| ood_double_gap | conditional_constant | guidance_scale | 2.5000 | 0.9500 | 0.0500 | 0.4427 | 3.5678 | 45.8824 | 0.0278 |
| ood_double_gap | constant | guidance_scale | 3.0000 | 0.9620 | 0.0380 | 0.6463 | 5.4441 | 55.5771 | 0.0280 |
| ood_double_gap | conditional_constant | guidance_scale | 3.0000 | 0.9640 | 0.0360 | 0.5002 | 5.7243 | 57.3029 | 0.0282 |
| ood_double_gap | constant | guidance_scale | 4.0000 | 0.9920 | 0.0080 | 0.8026 | 10.5147 | 77.1415 | 0.0276 |
| ood_double_gap | conditional_constant | guidance_scale | 4.0000 | 0.9860 | 0.0140 | 0.8661 | 11.4997 | 81.1638 | 0.0279 |
| ood_double_gap | constant | guidance_scale | 5.0000 | 0.9980 | 0.0020 | 0.9281 | 15.8535 | 95.5107 | 0.0284 |
| ood_double_gap | conditional_constant | guidance_scale | 5.0000 | 1.0000 | 0.0000 | 1.1181 | 17.3012 | 100.5029 | 0.0276 |
| ood_double_gap | distance_gated | guidance_scale | 0.0000 | 0.5580 | 0.4420 | 0.0609 | 0.2692 | 17.4148 | 0.0307 |
| ood_double_gap | conditional_distance_gated | guidance_scale | 0.0000 | 0.6900 | 0.3100 | 0.0503 | 0.2915 | 17.9051 | 0.0312 |
| ood_double_gap | distance_gated | guidance_scale | 0.5000 | 0.6780 | 0.3220 | 0.1497 | 0.3449 | 18.7421 | 0.0314 |
| ood_double_gap | conditional_distance_gated | guidance_scale | 0.5000 | 0.7780 | 0.2220 | 0.1714 | 0.3613 | 19.1067 | 0.0320 |
| ood_double_gap | distance_gated | guidance_scale | 1.0000 | 0.7440 | 0.2560 | 0.2519 | 0.5004 | 20.9544 | 0.0315 |
| ood_double_gap | conditional_distance_gated | guidance_scale | 1.0000 | 0.8340 | 0.1660 | 0.3048 | 0.5046 | 21.1592 | 0.0313 |
| ood_double_gap | distance_gated | guidance_scale | 1.5000 | 0.8100 | 0.1900 | 0.3188 | 0.7427 | 23.8579 | 0.0318 |
| ood_double_gap | conditional_distance_gated | guidance_scale | 1.5000 | 0.8720 | 0.1280 | 0.3358 | 0.7312 | 23.9139 | 0.0398 |
| ood_double_gap | distance_gated | guidance_scale | 2.0000 | 0.8540 | 0.1460 | 0.4992 | 1.0793 | 27.3239 | 0.0298 |
| ood_double_gap | conditional_distance_gated | guidance_scale | 2.0000 | 0.9140 | 0.0860 | 0.5683 | 1.0517 | 27.2729 | 0.0310 |
| ood_double_gap | distance_gated | guidance_scale | 2.5000 | 0.9160 | 0.0840 | 0.5931 | 1.5196 | 31.2680 | 0.0309 |
| ood_double_gap | conditional_distance_gated | guidance_scale | 2.5000 | 0.9420 | 0.0580 | 0.7311 | 1.4815 | 31.1848 | 0.0309 |
| ood_double_gap | distance_gated | guidance_scale | 3.0000 | 0.9480 | 0.0520 | 0.7318 | 2.0695 | 35.5963 | 0.0312 |
| ood_double_gap | conditional_distance_gated | guidance_scale | 3.0000 | 0.9780 | 0.0220 | 0.5774 | 2.0352 | 35.5953 | 0.0365 |
| ood_double_gap | distance_gated | guidance_scale | 4.0000 | 0.9800 | 0.0200 | 0.7718 | 3.4750 | 44.9015 | 0.0325 |
| ood_double_gap | conditional_distance_gated | guidance_scale | 4.0000 | 0.9820 | 0.0180 | 0.6724 | 3.5176 | 45.4724 | 0.0315 |
| ood_double_gap | distance_gated | guidance_scale | 5.0000 | 0.9940 | 0.0060 | 0.8918 | 5.1720 | 54.2869 | 0.0323 |
| ood_double_gap | conditional_distance_gated | guidance_scale | 5.0000 | 0.9940 | 0.0060 | 0.6586 | 5.4113 | 55.8220 | 0.0324 |
