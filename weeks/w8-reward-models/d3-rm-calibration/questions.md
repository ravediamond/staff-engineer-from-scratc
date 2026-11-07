# Questions

1. Define ECE. Why weight by bin size? What are its known weaknesses?
2. What does temperature scaling change and not change?
3. When does RM calibration matter, and when does it not?
4. How would you detect and fix length bias in an RM?
5. RM scores drift after the policy is updated (the new policy's outputs look different). What is happening and what do you do?

## Model answers

1. The sample-weighted average gap between confidence and accuracy across confidence bins. Weighting makes the metric reflect where predictions actually fall; unweighted, a bin with 1 sample counts as much as one with 1,000. Weaknesses: depends on binning (number of bins, equal-width vs equal-mass), can be gamed, says nothing about discrimination. Pair it with NLL or Brier score and reliability diagrams.
2. It rescales confidence (all margins divided by T) and leaves the ranking and accuracy unchanged. It fixes global over- or under-confidence, not slice-specific miscalibration.
3. It matters when scores feed thresholds or probabilistic decisions (data filtering, abstention, routing to humans, mixing rewards, KL-regularized RL where the reward scale interacts with β). It does not matter for pure ranking (best-of-N picks the argmax regardless).
4. Detect: correlation between reward and length on pairs of equal judged quality; reward as a function of artificially padded responses (append filler, check the reward rises); length-controlled win rates. Fix: length-balanced training pairs, adversarial padded negatives, length as a covariate regressed out, explicit length penalty at use time, and monitoring answer length during optimization.
5. Distribution shift: the RM was trained on outputs from earlier policies and the new outputs are out of distribution, where its errors are larger and exploitable. Refresh preference data on current policy samples (iterated or online RLHF), monitor the RM's agreement with held-out human or gold labels on new samples, use RM ensembles to detect high-uncertainty regions, and keep the KL constraint.
