# Guidance Ablation Summary

## Sweep Configuration

- `data_path`: `dataset/toy_trajectories.npy`
- `checkpoint_path`: `checkpoints/rectified_flow_mlp.pt`
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
| in_distribution_origin | baseline | guidance_scale | 0.0000 | 0.7280 | 0.2720 | 0.0735 | 0.2692 | 17.4148 | 0.0415 |
| in_distribution_origin | constant | guidance_scale | 0.0000 | 0.7280 | 0.2720 | 0.0735 | 0.2692 | 17.4148 | 0.0334 |
| in_distribution_origin | constant | guidance_scale | 0.5000 | 0.8100 | 0.1900 | 0.1677 | 0.4564 | 20.8372 | 0.0429 |
| in_distribution_origin | constant | guidance_scale | 1.0000 | 0.8260 | 0.1740 | 0.3039 | 0.8363 | 25.9498 | 0.0280 |
| in_distribution_origin | constant | guidance_scale | 1.5000 | 0.8720 | 0.1280 | 0.2939 | 1.4773 | 32.5574 | 0.0266 |
| in_distribution_origin | constant | guidance_scale | 2.0000 | 0.9220 | 0.0780 | 0.2746 | 2.4404 | 40.3244 | 0.0257 |
| in_distribution_origin | constant | guidance_scale | 2.5000 | 0.9720 | 0.0280 | 0.3913 | 3.7402 | 48.7776 | 0.0284 |
| in_distribution_origin | constant | guidance_scale | 3.0000 | 0.9820 | 0.0180 | 0.6567 | 5.3367 | 57.4689 | 0.0284 |
| in_distribution_origin | constant | guidance_scale | 4.0000 | 0.9920 | 0.0080 | 0.8411 | 9.0564 | 74.0421 | 0.0296 |
| in_distribution_origin | constant | guidance_scale | 5.0000 | 1.0000 | 0.0000 | 1.0180 | 12.7621 | 87.7576 | 0.0267 |
| in_distribution_origin | distance_gated | guidance_scale | 0.0000 | 0.7280 | 0.2720 | 0.0735 | 0.2692 | 17.4148 | 0.0339 |
| in_distribution_origin | distance_gated | guidance_scale | 0.5000 | 0.8000 | 0.2000 | 0.1625 | 0.3999 | 19.8482 | 0.0296 |
| in_distribution_origin | distance_gated | guidance_scale | 1.0000 | 0.8220 | 0.1780 | 0.1167 | 0.6324 | 23.2087 | 0.0292 |
| in_distribution_origin | distance_gated | guidance_scale | 1.5000 | 0.8460 | 0.1540 | 0.2489 | 0.9623 | 27.1347 | 0.0301 |
| in_distribution_origin | distance_gated | guidance_scale | 2.0000 | 0.9000 | 0.1000 | 0.3563 | 1.3783 | 31.3289 | 0.0308 |
| in_distribution_origin | distance_gated | guidance_scale | 2.5000 | 0.9420 | 0.0580 | 0.4250 | 1.8673 | 35.5893 | 0.0299 |
| in_distribution_origin | distance_gated | guidance_scale | 3.0000 | 0.9800 | 0.0200 | 0.6033 | 2.4153 | 39.7850 | 0.0301 |
| in_distribution_origin | distance_gated | guidance_scale | 4.0000 | 0.9900 | 0.0100 | 0.4468 | 3.6238 | 47.7035 | 0.0285 |
| in_distribution_origin | distance_gated | guidance_scale | 5.0000 | 0.9960 | 0.0040 | 0.7809 | 4.8701 | 54.7001 | 0.0288 |
| ood_shifted_y | baseline | guidance_scale | 0.0000 | 0.7620 | 0.2380 | 0.0767 | 0.2692 | 17.4148 | 0.0234 |
| ood_shifted_y | constant | guidance_scale | 0.0000 | 0.7620 | 0.2380 | 0.0767 | 0.2692 | 17.4148 | 0.0260 |
| ood_shifted_y | constant | guidance_scale | 0.5000 | 0.9160 | 0.0840 | 0.1232 | 0.3120 | 18.1545 | 0.0286 |
| ood_shifted_y | constant | guidance_scale | 1.0000 | 0.9660 | 0.0340 | 0.2837 | 0.3707 | 19.0707 | 0.0277 |
| ood_shifted_y | constant | guidance_scale | 1.5000 | 0.9980 | 0.0020 | 0.5692 | 0.4332 | 20.0194 | 0.0281 |
| ood_shifted_y | constant | guidance_scale | 2.0000 | 1.0000 | 0.0000 | 1.0709 | 0.4964 | 20.9451 | 0.0270 |
| ood_shifted_y | constant | guidance_scale | 2.5000 | 1.0000 | 0.0000 | 1.1662 | 0.5605 | 21.8376 | 0.0286 |
| ood_shifted_y | constant | guidance_scale | 3.0000 | 1.0000 | 0.0000 | 1.4181 | 0.6249 | 22.6936 | 0.0289 |
| ood_shifted_y | constant | guidance_scale | 4.0000 | 1.0000 | 0.0000 | 1.6194 | 0.7527 | 24.2692 | 0.0260 |
| ood_shifted_y | constant | guidance_scale | 5.0000 | 1.0000 | 0.0000 | 1.6387 | 0.8728 | 25.6210 | 0.0286 |
| ood_shifted_y | distance_gated | guidance_scale | 0.0000 | 0.7620 | 0.2380 | 0.0767 | 0.2692 | 17.4148 | 0.0322 |
| ood_shifted_y | distance_gated | guidance_scale | 0.5000 | 0.8940 | 0.1060 | 0.2353 | 0.2956 | 17.8406 | 0.0317 |
| ood_shifted_y | distance_gated | guidance_scale | 1.0000 | 0.9380 | 0.0620 | 0.4050 | 0.3357 | 18.4296 | 0.0323 |
| ood_shifted_y | distance_gated | guidance_scale | 1.5000 | 0.9720 | 0.0280 | 0.3500 | 0.3768 | 19.0229 | 0.0312 |
| ood_shifted_y | distance_gated | guidance_scale | 2.0000 | 0.9900 | 0.0100 | 0.5884 | 0.4161 | 19.5821 | 0.0321 |
| ood_shifted_y | distance_gated | guidance_scale | 2.5000 | 0.9960 | 0.0040 | 0.7441 | 0.4533 | 20.0997 | 0.0303 |
| ood_shifted_y | distance_gated | guidance_scale | 3.0000 | 0.9980 | 0.0020 | 0.4836 | 0.4882 | 20.5759 | 0.0317 |
| ood_shifted_y | distance_gated | guidance_scale | 4.0000 | 0.9980 | 0.0020 | 0.9639 | 0.5490 | 21.4027 | 0.0306 |
| ood_shifted_y | distance_gated | guidance_scale | 5.0000 | 1.0000 | 0.0000 | 1.2500 | 0.6015 | 22.0902 | 0.0303 |
| ood_double_gap | baseline | guidance_scale | 0.0000 | 0.5580 | 0.4420 | 0.0609 | 0.2692 | 17.4148 | 0.0239 |
| ood_double_gap | constant | guidance_scale | 0.0000 | 0.5580 | 0.4420 | 0.0609 | 0.2692 | 17.4148 | 0.0294 |
| ood_double_gap | constant | guidance_scale | 0.5000 | 0.6900 | 0.3100 | 0.1623 | 0.3853 | 19.4416 | 0.0283 |
| ood_double_gap | constant | guidance_scale | 1.0000 | 0.7700 | 0.2300 | 0.2169 | 0.6606 | 23.1349 | 0.0285 |
| ood_double_gap | constant | guidance_scale | 1.5000 | 0.8240 | 0.1760 | 0.3185 | 1.1894 | 28.6431 | 0.0277 |
| ood_double_gap | constant | guidance_scale | 2.0000 | 0.9060 | 0.0940 | 0.3796 | 2.0981 | 36.0621 | 0.0303 |
| ood_double_gap | constant | guidance_scale | 2.5000 | 0.9400 | 0.0600 | 0.6782 | 3.5037 | 45.1970 | 0.0287 |
| ood_double_gap | constant | guidance_scale | 3.0000 | 0.9620 | 0.0380 | 0.6463 | 5.4441 | 55.5771 | 0.0290 |
| ood_double_gap | constant | guidance_scale | 4.0000 | 0.9920 | 0.0080 | 0.8026 | 10.5147 | 77.1415 | 0.0292 |
| ood_double_gap | constant | guidance_scale | 5.0000 | 0.9980 | 0.0020 | 0.9281 | 15.8535 | 95.5107 | 0.0307 |
| ood_double_gap | distance_gated | guidance_scale | 0.0000 | 0.5580 | 0.4420 | 0.0609 | 0.2692 | 17.4148 | 0.0329 |
| ood_double_gap | distance_gated | guidance_scale | 0.5000 | 0.6780 | 0.3220 | 0.1497 | 0.3449 | 18.7421 | 0.0353 |
| ood_double_gap | distance_gated | guidance_scale | 1.0000 | 0.7440 | 0.2560 | 0.2519 | 0.5004 | 20.9544 | 0.0334 |
| ood_double_gap | distance_gated | guidance_scale | 1.5000 | 0.8100 | 0.1900 | 0.3188 | 0.7427 | 23.8579 | 0.0343 |
| ood_double_gap | distance_gated | guidance_scale | 2.0000 | 0.8540 | 0.1460 | 0.4992 | 1.0793 | 27.3239 | 0.0333 |
| ood_double_gap | distance_gated | guidance_scale | 2.5000 | 0.9160 | 0.0840 | 0.5931 | 1.5196 | 31.2680 | 0.0323 |
| ood_double_gap | distance_gated | guidance_scale | 3.0000 | 0.9480 | 0.0520 | 0.7318 | 2.0695 | 35.5963 | 0.0321 |
| ood_double_gap | distance_gated | guidance_scale | 4.0000 | 0.9800 | 0.0200 | 0.7718 | 3.4750 | 44.9015 | 0.0337 |
| ood_double_gap | distance_gated | guidance_scale | 5.0000 | 0.9940 | 0.0060 | 0.8918 | 5.1720 | 54.2869 | 0.0322 |

## Scenario Mean Summary

| Scenario | Decay | Param | Value | Success Rate | Collision Rate | Min Distance | Smoothness | Path Length | Time (s) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| in_distribution_origin | baseline | guidance_scale | 0.0000 | 0.7280 | 0.2720 | 0.0735 | 0.2692 | 17.4148 | 0.0415 |
| in_distribution_origin | constant | guidance_scale | 0.0000 | 0.7280 | 0.2720 | 0.0735 | 0.2692 | 17.4148 | 0.0334 |
| in_distribution_origin | constant | guidance_scale | 0.5000 | 0.8100 | 0.1900 | 0.1677 | 0.4564 | 20.8372 | 0.0429 |
| in_distribution_origin | constant | guidance_scale | 1.0000 | 0.8260 | 0.1740 | 0.3039 | 0.8363 | 25.9498 | 0.0280 |
| in_distribution_origin | constant | guidance_scale | 1.5000 | 0.8720 | 0.1280 | 0.2939 | 1.4773 | 32.5574 | 0.0266 |
| in_distribution_origin | constant | guidance_scale | 2.0000 | 0.9220 | 0.0780 | 0.2746 | 2.4404 | 40.3244 | 0.0257 |
| in_distribution_origin | constant | guidance_scale | 2.5000 | 0.9720 | 0.0280 | 0.3913 | 3.7402 | 48.7776 | 0.0284 |
| in_distribution_origin | constant | guidance_scale | 3.0000 | 0.9820 | 0.0180 | 0.6567 | 5.3367 | 57.4689 | 0.0284 |
| in_distribution_origin | constant | guidance_scale | 4.0000 | 0.9920 | 0.0080 | 0.8411 | 9.0564 | 74.0421 | 0.0296 |
| in_distribution_origin | constant | guidance_scale | 5.0000 | 1.0000 | 0.0000 | 1.0180 | 12.7621 | 87.7576 | 0.0267 |
| in_distribution_origin | distance_gated | guidance_scale | 0.0000 | 0.7280 | 0.2720 | 0.0735 | 0.2692 | 17.4148 | 0.0339 |
| in_distribution_origin | distance_gated | guidance_scale | 0.5000 | 0.8000 | 0.2000 | 0.1625 | 0.3999 | 19.8482 | 0.0296 |
| in_distribution_origin | distance_gated | guidance_scale | 1.0000 | 0.8220 | 0.1780 | 0.1167 | 0.6324 | 23.2087 | 0.0292 |
| in_distribution_origin | distance_gated | guidance_scale | 1.5000 | 0.8460 | 0.1540 | 0.2489 | 0.9623 | 27.1347 | 0.0301 |
| in_distribution_origin | distance_gated | guidance_scale | 2.0000 | 0.9000 | 0.1000 | 0.3563 | 1.3783 | 31.3289 | 0.0308 |
| in_distribution_origin | distance_gated | guidance_scale | 2.5000 | 0.9420 | 0.0580 | 0.4250 | 1.8673 | 35.5893 | 0.0299 |
| in_distribution_origin | distance_gated | guidance_scale | 3.0000 | 0.9800 | 0.0200 | 0.6033 | 2.4153 | 39.7850 | 0.0301 |
| in_distribution_origin | distance_gated | guidance_scale | 4.0000 | 0.9900 | 0.0100 | 0.4468 | 3.6238 | 47.7035 | 0.0285 |
| in_distribution_origin | distance_gated | guidance_scale | 5.0000 | 0.9960 | 0.0040 | 0.7809 | 4.8701 | 54.7001 | 0.0288 |
| ood_shifted_y | baseline | guidance_scale | 0.0000 | 0.7620 | 0.2380 | 0.0767 | 0.2692 | 17.4148 | 0.0234 |
| ood_shifted_y | constant | guidance_scale | 0.0000 | 0.7620 | 0.2380 | 0.0767 | 0.2692 | 17.4148 | 0.0260 |
| ood_shifted_y | constant | guidance_scale | 0.5000 | 0.9160 | 0.0840 | 0.1232 | 0.3120 | 18.1545 | 0.0286 |
| ood_shifted_y | constant | guidance_scale | 1.0000 | 0.9660 | 0.0340 | 0.2837 | 0.3707 | 19.0707 | 0.0277 |
| ood_shifted_y | constant | guidance_scale | 1.5000 | 0.9980 | 0.0020 | 0.5692 | 0.4332 | 20.0194 | 0.0281 |
| ood_shifted_y | constant | guidance_scale | 2.0000 | 1.0000 | 0.0000 | 1.0709 | 0.4964 | 20.9451 | 0.0270 |
| ood_shifted_y | constant | guidance_scale | 2.5000 | 1.0000 | 0.0000 | 1.1662 | 0.5605 | 21.8376 | 0.0286 |
| ood_shifted_y | constant | guidance_scale | 3.0000 | 1.0000 | 0.0000 | 1.4181 | 0.6249 | 22.6936 | 0.0289 |
| ood_shifted_y | constant | guidance_scale | 4.0000 | 1.0000 | 0.0000 | 1.6194 | 0.7527 | 24.2692 | 0.0260 |
| ood_shifted_y | constant | guidance_scale | 5.0000 | 1.0000 | 0.0000 | 1.6387 | 0.8728 | 25.6210 | 0.0286 |
| ood_shifted_y | distance_gated | guidance_scale | 0.0000 | 0.7620 | 0.2380 | 0.0767 | 0.2692 | 17.4148 | 0.0322 |
| ood_shifted_y | distance_gated | guidance_scale | 0.5000 | 0.8940 | 0.1060 | 0.2353 | 0.2956 | 17.8406 | 0.0317 |
| ood_shifted_y | distance_gated | guidance_scale | 1.0000 | 0.9380 | 0.0620 | 0.4050 | 0.3357 | 18.4296 | 0.0323 |
| ood_shifted_y | distance_gated | guidance_scale | 1.5000 | 0.9720 | 0.0280 | 0.3500 | 0.3768 | 19.0229 | 0.0312 |
| ood_shifted_y | distance_gated | guidance_scale | 2.0000 | 0.9900 | 0.0100 | 0.5884 | 0.4161 | 19.5821 | 0.0321 |
| ood_shifted_y | distance_gated | guidance_scale | 2.5000 | 0.9960 | 0.0040 | 0.7441 | 0.4533 | 20.0997 | 0.0303 |
| ood_shifted_y | distance_gated | guidance_scale | 3.0000 | 0.9980 | 0.0020 | 0.4836 | 0.4882 | 20.5759 | 0.0317 |
| ood_shifted_y | distance_gated | guidance_scale | 4.0000 | 0.9980 | 0.0020 | 0.9639 | 0.5490 | 21.4027 | 0.0306 |
| ood_shifted_y | distance_gated | guidance_scale | 5.0000 | 1.0000 | 0.0000 | 1.2500 | 0.6015 | 22.0902 | 0.0303 |
| ood_double_gap | baseline | guidance_scale | 0.0000 | 0.5580 | 0.4420 | 0.0609 | 0.2692 | 17.4148 | 0.0239 |
| ood_double_gap | constant | guidance_scale | 0.0000 | 0.5580 | 0.4420 | 0.0609 | 0.2692 | 17.4148 | 0.0294 |
| ood_double_gap | constant | guidance_scale | 0.5000 | 0.6900 | 0.3100 | 0.1623 | 0.3853 | 19.4416 | 0.0283 |
| ood_double_gap | constant | guidance_scale | 1.0000 | 0.7700 | 0.2300 | 0.2169 | 0.6606 | 23.1349 | 0.0285 |
| ood_double_gap | constant | guidance_scale | 1.5000 | 0.8240 | 0.1760 | 0.3185 | 1.1894 | 28.6431 | 0.0277 |
| ood_double_gap | constant | guidance_scale | 2.0000 | 0.9060 | 0.0940 | 0.3796 | 2.0981 | 36.0621 | 0.0303 |
| ood_double_gap | constant | guidance_scale | 2.5000 | 0.9400 | 0.0600 | 0.6782 | 3.5037 | 45.1970 | 0.0287 |
| ood_double_gap | constant | guidance_scale | 3.0000 | 0.9620 | 0.0380 | 0.6463 | 5.4441 | 55.5771 | 0.0290 |
| ood_double_gap | constant | guidance_scale | 4.0000 | 0.9920 | 0.0080 | 0.8026 | 10.5147 | 77.1415 | 0.0292 |
| ood_double_gap | constant | guidance_scale | 5.0000 | 0.9980 | 0.0020 | 0.9281 | 15.8535 | 95.5107 | 0.0307 |
| ood_double_gap | distance_gated | guidance_scale | 0.0000 | 0.5580 | 0.4420 | 0.0609 | 0.2692 | 17.4148 | 0.0329 |
| ood_double_gap | distance_gated | guidance_scale | 0.5000 | 0.6780 | 0.3220 | 0.1497 | 0.3449 | 18.7421 | 0.0353 |
| ood_double_gap | distance_gated | guidance_scale | 1.0000 | 0.7440 | 0.2560 | 0.2519 | 0.5004 | 20.9544 | 0.0334 |
| ood_double_gap | distance_gated | guidance_scale | 1.5000 | 0.8100 | 0.1900 | 0.3188 | 0.7427 | 23.8579 | 0.0343 |
| ood_double_gap | distance_gated | guidance_scale | 2.0000 | 0.8540 | 0.1460 | 0.4992 | 1.0793 | 27.3239 | 0.0333 |
| ood_double_gap | distance_gated | guidance_scale | 2.5000 | 0.9160 | 0.0840 | 0.5931 | 1.5196 | 31.2680 | 0.0323 |
| ood_double_gap | distance_gated | guidance_scale | 3.0000 | 0.9480 | 0.0520 | 0.7318 | 2.0695 | 35.5963 | 0.0321 |
| ood_double_gap | distance_gated | guidance_scale | 4.0000 | 0.9800 | 0.0200 | 0.7718 | 3.4750 | 44.9015 | 0.0337 |
| ood_double_gap | distance_gated | guidance_scale | 5.0000 | 0.9940 | 0.0060 | 0.8918 | 5.1720 | 54.2869 | 0.0322 |
