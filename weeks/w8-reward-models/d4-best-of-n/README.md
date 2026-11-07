# W8 D4: best-of-N and reward over-optimisation

Primer: `knowledge/08-reward-models-and-preference-learning.md` §4.
Reference: Gao, Schulman, Hilton, "Scaling Laws for Reward Model Overoptimization" (2022).

## The one idea

**Best-of-N (BoN):** sample N responses, return the one the reward model scores highest. Simple,
strong, no training. Its distance from the base policy has a closed form:

```
KL(BoN || base) = log N − (N − 1) / N
```

As N grows you optimise harder against the **proxy** RM. The proxy score keeps rising; the
**gold** (true) reward rises, peaks, then **falls**: the optimiser finds the proxy's mistakes
(Goodhart's law). Gao et al. measured exactly this curve against KL.

Today's toy world: each sample has a true quality `q` and a length `l`. The proxy RM likes length
(`proxy = q + 1.5·l`); the gold reward penalises verbosity (`gold = q − 0.3·l²`). Sweep N and watch.

**The cardinal rule:** never report the quality of selected samples using the **same RM that selected
them**. That number is biased upward by construction (winner's curse). Evaluate with a held-out
judge, humans, or the gold function.

## Today's build (`w8d4_bon.py`)

`bon_kl(n)`, `sample(rng)` (provided), `proxy`, `gold`, `best_of_n(samples, score_fn)`,
`overoptimization_curve(ns, trials, seed)` → `[(n, kl, mean_proxy, mean_gold)]`, `gold_peak_n(curve)`.

## Staff angle

Every team that adds "generate 8, pick the best with our judge" ships this failure mode, and the
dashboards look great because they report the judge's score. The staff move: separate the
selection model from the evaluation model, plot gold-vs-N on a sample, and set N at the peak
(often small) instead of "more is better".
