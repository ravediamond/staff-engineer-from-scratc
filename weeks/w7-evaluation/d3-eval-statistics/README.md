# W7 D3: statistics for evals

Primer: `knowledge/07-evaluation-and-experimentation.md` §2.

## The one idea

Five tools cover most eval claims:

| Tool | Question | Formula / method |
|---|---|---|
| **Wilson interval** | CI for a pass rate (better than ±1.96·√(p(1−p)/n) near 0 or 1) | center `(p + z²/2n)/(1 + z²/n)`, half-width `z·√(p(1−p)/n + z²/4n²)/(1 + z²/n)` |
| **McNemar** | are two systems' pass rates different on the same cases? | only **discordant** pairs matter: b (A pass, B fail), c (A fail, B pass); exact two-sided binomial test of b vs Binomial(b+c, 0.5) |
| **Holm–Bonferroni** | testing 12 slices: which differences survive? | sort p-values; reject `p_(i) ≤ α/(m−i+1)` until the first failure |
| **Sample size** | how many cases to detect a 5-point difference? | two proportions: `n = (z_{α/2}·√(2p̄(1−p̄)) + z_β·√(p1(1−p1)+p2(1−p2)))² / (p1−p2)²` per arm |
| **Minimum detectable effect** | what can my 200-case set resolve? | invert the formula above |

## Today's build (`w7d3_stats.py`)

`wilson(successes, n, z=1.96)`, `mcnemar_exact(b, c)`, `holm(pvals, alpha)`,
`n_per_arm(p1, p2, alpha, power)`, `mde(n, p, alpha, power)` (by search). `statistics.NormalDist` only, no scipy.

## Staff angle

Saying "we need 1,600 cases to detect a 3-point change, we have 200, so this eval can only see
10-point changes" is a staff sentence. It re-scopes the conversation from "which prompt won" to
"is our instrument good enough to decide", and usually unblocks budget for labelling.
