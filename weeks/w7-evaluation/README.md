# Week 7: evaluation and experimentation

This is your specialty, so the bar is higher: not "I built an eval tool" but "I can tell you,
with a confidence interval, whether this change is better, for whom, and whether the offline
number predicts what users will feel". The labs build the statistics you should be able to
derive on a whiteboard, the judge-calibration checks most teams skip, and the online
experimentation tools (SRM, CUPED, peeking) that product teams get wrong.

Primer: `knowledge/07-evaluation-and-experimentation.md`.

| Day | Lab | Review bug |
|---|---|---|
| d1 | eval harness: repeats, flakiness, slices, paired bootstrap, regression gate | unpaired bootstrap hides a real regression |
| d2 | LLM-as-judge calibration: kappa, weighted kappa, position bias | kappa's chance agreement uses one rater's marginals |
| d3 | statistics for evals: Wilson, McNemar, Holm, sample size | McNemar divides by all pairs |
| d4 | online A/B: SRM, two-proportion test, CUPED, peeking | CUPED θ uses var(y) |
| d5 | offline ↔ online agreement, launch rules + **Friday design** | Kendall τ denominator off by 2× |
