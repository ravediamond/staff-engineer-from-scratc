# Questions

1. Best-of-N: what is it, what is its KL from the base policy, and why does that formula matter?
2. Explain reward over-optimisation with the curve. What sets the peak?
3. Why is evaluating BoN picks with the selecting RM biased?
4. How do you pick N in production?
5. Mitigations for over-optimisation in RLHF and in BoN.

## Model answers

1. Sample N, keep the RM's argmax. KL = log N − (N−1)/N: it grows only logarithmically, so BoN is a "gentle" optimizer and a calibrated way to compare optimization pressure with RL at matched KL (Gao et al. plot gold reward against √KL).
2. As optimization pressure (N or KL) grows, proxy reward rises monotonically while gold reward rises then falls, because the optimizer moves into regions where the proxy's errors are large and correlated with what it rewards (length, style, sycophancy). The peak depends on RM quality (size, data), the base policy, and how exploitable the RM's errors are.
3. The pick is the max of N noisy scores, so its score includes the largest positive error among N (winner's curse / regression to the mean); the expected bias grows with N. An independent judge or human labels remove the selection bias.
4. Measure gold quality (human or independent judge) against N on a representative sample; choose the smallest N inside the CI of the peak, then weigh it against cost (N× generation) and latency. Re-check when the RM or the policy changes.
5. KL penalty to a reference policy, RM ensembles (pessimistic aggregation, uncertainty penalties), larger and better RMs, refreshing preference data on current policy outputs, early stopping on held-out gold or judge metrics, length penalties and constraint-style rewards, and for BoN: smaller N or a different model for selection and evaluation.
