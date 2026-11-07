# Questions

1. Why Wilson over the normal approximation for pass rates?
2. Explain McNemar in one sentence. Why do concordant pairs not matter?
3. You test 15 slices. How do you report which ones regressed?
4. Your PM wants to detect a 2-point change on a 75% pass rate. How many cases? What do you propose instead?
5. Bootstrap vs analytic tests: when do you use each?

## Model answers

1. The normal interval can extend below 0 or above 1 and has poor coverage for small n or p near 0/1 (e.g. 0/20 gives [0, 0]). Wilson inverts the score test and stays in [0, 1] with near-nominal coverage.
2. It tests whether the two kinds of disagreement (A right/B wrong vs A wrong/B right) are equally likely. Cases where both pass or both fail carry no information about which system is better.
3. Holm (controls family-wise error) or Benjamini–Hochberg (controls false discovery rate, more power) over the 15 p-values, reporting the adjusted results and the effect sizes with CIs, plus a pre-declared list of critical slices tested at full alpha.
4. n_per_arm(0.75, 0.77) ≈ 7,000 per arm unpaired (fewer paired, but still thousands). Propose: use a paired design (much smaller n), accept a larger MDE (5 points ≈ 1,100), focus on the slices where the change is expected to matter, or use a more sensitive continuous metric.
5. Bootstrap: any statistic (nDCG, medians, ratios), clustered data (resample clusters), few assumptions; costs compute and needs enough samples (unreliable for very small n). Analytic: fast and exact for standard cases (proportions, McNemar), useful for power planning before you have data.
