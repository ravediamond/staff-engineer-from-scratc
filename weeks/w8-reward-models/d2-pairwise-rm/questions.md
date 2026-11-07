# Questions

1. Write the pairwise RM loss and the step-0 value.
2. Why can't RM accuracy reach 100% on human preference data? What bounds it?
3. Why split by prompt? What other leakage paths exist in preference data?
4. Pairwise vs pointwise (absolute score) reward models: trade-offs.
5. How would you collect 100k preference pairs for a domain assistant, and what quality controls?

## Model answers

1. L = −E[log σ(r(x, y_c) − r(x, y_r))]. At init r_c ≈ r_r, so L ≈ log 2 ≈ 0.693. If you see something else at step 0, check the data or the model.
2. Labels are noisy: annotators disagree on close pairs, and preferences are not deterministic. Inter-annotator agreement (often 65–80%) bounds achievable accuracy; the Bayes-optimal accuracy under BT noise is E[max(p, 1−p)].
3. Pairs from the same prompt share context features; the model can memorize prompt-specific shortcuts, and evaluation then measures memorization. Other leaks: near-duplicate prompts across splits (dedupe with MinHash), the same responses reused across prompts, temporal leakage (test from an earlier period than train), and annotator leakage (the same annotator style in both splits when you want to generalize across annotators).
4. Pairwise: easier and more consistent for humans, matches BT, no absolute calibration needed, but scores are only meaningful relative to each other and need pairs. Pointwise (e.g. 1–7 ratings): cheaper per item and usable for filtering, but suffers annotator scale drift and lower reliability. Common hybrid: pairwise plus a margin/strength label.
5. Sample prompts from real traffic (stratified by intent), generate 2–4 responses from diverse policies or temperatures, use domain-expert annotators with written guidelines and examples, overlap 10–20% of items for agreement measurement, include gold items for annotator QA, add a "tie or both bad" option, measure per-annotator agreement and drop low-agreement annotators, version and audit the data, and run a pilot of 1k pairs to refine the guidelines before scaling.
