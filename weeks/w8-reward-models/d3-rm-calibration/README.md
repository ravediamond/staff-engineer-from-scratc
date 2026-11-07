# W8 D3: reward-model calibration and length bias

Primer: `knowledge/08-reward-models-and-preference-learning.md` §3.

## The one idea

An RM outputs a margin `m = r_c − r_r`; `σ(m)` claims a probability that "chosen" is preferred.
Is that probability honest?

**Expected calibration error (ECE):** bin predictions by confidence, compare mean confidence with
empirical accuracy in each bin, **weight each bin by its share of samples**:
`ECE = Σ_b (n_b / N) · |acc_b − conf_b|`. Unweighted ECE lets a near-empty bin dominate.

**Temperature scaling:** fit one scalar `T > 0` minimising NLL of `σ(m / T)` on held-out pairs.
It does not change accuracy (ranking is preserved), only confidence. Optimise `log T` so T stays positive.

**Length bias:** RMs trained on human data often learn "longer = better". Measure the correlation
between reward and length on responses of **equal true quality**; then a policy optimised against
the RM gets verbose (D4). Mitigations: length-balanced training pairs, a length penalty, or length
as an explicit covariate that is removed at use time.

## Today's build (`w8d3_calibration.py`)

`ece(probs, labels, n_bins)`, `fit_temperature(margins, labels, steps, lr)`, `nll(margins, labels, T)`,
`pearson(x, y)`, `length_bias(rewards, lengths)`.

## Staff angle

Calibration matters the moment someone uses RM scores as a **threshold** (filter training data,
gate releases, route to humans) instead of only for ranking. A staff review asks "what decision
consumes this score, and is it calibrated for that decision?" before anyone ships "reward > 0.7".
