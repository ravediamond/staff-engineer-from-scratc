# W7 D2: LLM-as-judge calibration

Primer: `knowledge/07-evaluation-and-experimentation.md` §3.

## The one idea

An LLM judge is a measurement instrument with **unknown bias** until you calibrate it against
humans. Three checks every team should run before trusting a judge:

1. **Agreement beyond chance: Cohen's κ.**
   `κ = (p_o − p_e) / (1 − p_e)`, with `p_o` observed agreement and `p_e = Σ_c p_A(c)·p_B(c)` the
   chance agreement from **both** raters' marginals. 90% raw agreement on a 90/10 label split can be
   κ ≈ 0. Rough reading: < 0.4 poor, 0.4–0.6 moderate, 0.6–0.8 substantial, > 0.8 near-perfect.
2. **Ordinal scales: weighted κ** (quadratic weights): disagreeing 1 vs 5 costs more than 4 vs 5.
3. **Position bias** for pairwise judges: ask (A, B) and (B, A). A consistent judge flips its answer.
   Report the consistency rate; use both orders and count only consistent verdicts (or ties).

Also known: verbosity bias (longer answers win), self-preference (a model prefers its own outputs).

## Today's build (`w7d2_judge.py`)

`confusion(a, b, labels)`, `cohen_kappa(a, b)`, `weighted_kappa(a, b, labels)` (quadratic),
`position_consistency(verdicts_ab, verdicts_ba)`, `debiased_verdicts(verdicts_ab, verdicts_ba)`.

## Staff angle

Judges are how evaluation scales; uncalibrated judges are how organisations fool themselves at
scale. The staff practice: a small, expensive, human-labelled calibration set (200–500 items,
2+ annotators, their own κ reported first: the judge cannot be expected to beat the humans'
agreement), judge κ vs humans reported next to every judge-based metric, and recalibration
whenever the judge model or prompt changes.
