# 07. Evaluation and experimentation

## §1 The eval harness as an instrument

Versioned datasets with slices and provenance; runs tied to system fingerprints (prompt, model, tools,
config hashes); repeats for non-determinism; flaky-case reporting; deterministic scorers before judges;
results stored immutably; reports on the PR.

## §2 Statistics you must be able to derive

- Paired bootstrap of the mean difference (resample cases).
- Wilson interval for pass rates.
- McNemar exact test on discordant pairs.
- Holm or Benjamini–Hochberg for many slices.
- Sample size for two proportions; minimum detectable effect of your dataset.
- With 200 cases, an eval resolves ~8–10 point differences on 80% pass rates (unpaired); pairing helps a lot.

## §3 LLM judges

Calibrate against humans: Cohen's κ (raw agreement lies on skewed labels), weighted κ for ordinal scales,
position-bias checks (both orders), verbosity bias, self-preference. Human-human κ is the ceiling.
Recalibrate whenever the judge model or prompt changes.

## §4 Online experiments

SRM check before anything; pooled two-proportion z-test; CUPED with a pre-period covariate (variance × (1 − ρ²));
no peeking without sequential methods; randomise at the user level for anything with memory; metric hierarchy:
one primary, guardrails that veto, diagnostics.

## §5 Offline ↔ online

Track, for every launch, the offline delta and the online delta. Kendall τ across model versions and sign
agreement across launches tell you whether your offline evals predict users. Retire metrics that do not.

## The eval maturity ladder (use it to describe teams, including your own)

1. Vibes and demos. 2. A notebook with a fixed set. 3. A harness in CI with averages. 4. Paired statistics,
slices, calibrated judges, gates. 5. Offline ↔ online tracking, eval sets grown from incidents, governance.

## Questions

1. An exec asks "is the new model better?" You have 300 eval cases and a week. What do you do?
<details><summary>Answer</summary>Paired evaluation on the 300 cases with CIs and per-slice results; read 30 changed outputs; check cost and latency; if the gain is inside the MDE, say "not distinguishable at this size". In parallel, a small online test (if the product allows) with guardrails. Answer with a decision recommendation and the uncertainty, not just a number.</details>

2. How do you evaluate an agent (multi-step, tools) rather than a single response?
<details><summary>Answer</summary>Task-level success with verifiable end states (tests pass, record created, answer matches), on a task set with recorded or sandboxed environments; trajectory metrics (steps, tool errors, loops, cost); process checks on critical steps; repeats for variance (pass@k vs pass^k: success rate across repeated runs matters for reliability); slices by task type.</details>

3. What is benchmark contamination and how do you guard against it?
<details><summary>Answer</summary>Test items or close variants leaked into training or prompt-tuning data, inflating scores. Guard: private held-out sets, canary strings, n-gram overlap checks against training data, refresh sets over time, and comparison of performance on pre- vs post-cutoff items.</details>
