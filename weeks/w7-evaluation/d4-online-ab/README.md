# W7 D4: online A/B testing: SRM, z-test, CUPED, peeking

Primer: `knowledge/07-evaluation-and-experimentation.md` §4.

## The one idea

Offline evals approximate users; online experiments measure them. Four things that go wrong:

1. **Sample ratio mismatch (SRM).** You split 50/50 and observe 50,912 vs 49,088. A chi-square test
   (df = 1) says if that is chance. If p < 0.001, **stop**: assignment or logging is broken, every
   metric is suspect.
2. **The test itself.** Two proportions: pooled z-test, `z = (p_b − p_a) / √(p̂(1−p̂)(1/n_a + 1/n_b))`.
3. **Variance.** **CUPED** (Deng et al., Microsoft, 2013): use a pre-experiment covariate x (last month's
   metric for the same user), `y' = y − θ(x − x̄)` with `θ = cov(x, y) / var(x)`. Variance drops by a
   factor `1 − ρ²`: with ρ = 0.7, ~50% fewer users for the same power.
4. **Peeking.** Checking p < 0.05 every day and stopping at the first success inflates the false
   positive rate far above 5%. Fix: fixed horizon, or alpha spending / sequential tests (today: the
   simple Bonferroni-across-looks version, and a simulation of the inflation).

## Today's build (`w7d4_ab.py`)

`srm_pvalue(n_a, n_b, ratio)`, `two_prop_z(conv_a, n_a, conv_b, n_b) -> (z, p)`, `cuped(y, x) -> (y_adj, theta)`,
`variance_reduction(y, x)`, `peeking_false_positive_rate(n_sims, looks, n_per_look, alpha, seed, correct)`.

## Staff angle

For LLM features, the primary metric is rarely clean: "thumbs up rate" is biased toward users who
vote, "retention" is slow. A staff design defines a metric hierarchy before launch: one primary
(decision) metric, guardrails that can veto (latency, cost per user, safety reports, complaint
rate), and diagnostic metrics. And it decides the unit of randomisation (user, not request, for
anything with memory or learning effects).
