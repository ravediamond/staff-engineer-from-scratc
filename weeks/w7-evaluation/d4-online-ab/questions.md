# Questions

1. What is SRM, what causes it, and what do you do when you detect it?
2. Derive why CUPED reduces variance by 1 − ρ², and say what covariate you would use for an LLM assistant.
3. Why is peeking a problem, and what are the proper alternatives?
4. Unit of randomisation for (a) a new reranker, (b) a memory feature in an assistant, (c) a pricing change.
5. Define the metric hierarchy for launching a new model in a consumer assistant.

## Model answers

1. The observed split differs from the designed split beyond chance. Causes: buggy assignment, bots filtered differently per arm, crashes or redirects losing users in one arm, logging bugs, triggering conditions that depend on the treatment. Stop the analysis, find the cause (check by platform, day, browser), fix it, restart. Any metric from an SRM experiment is untrustworthy.
2. var(y − θx) = var(y) − 2θcov + θ²var(x), minimized at θ = cov/var(x) to var(y)(1 − ρ²). The mean is unchanged because E[x − x̄] = 0, and x is pre-treatment so it is independent of assignment. For an assistant: the same user's pre-period value of the metric (sessions, messages, thumbs-up rate) or engagement level.
3. Each look is another chance to cross the threshold by noise; stopping at the first crossing inflates the false positive rate (~20% with 10 looks). Alternatives: fixed horizon decided by a power calculation; group-sequential designs with alpha spending (O'Brien–Fleming); always-valid inference (mSPRT); Bayesian approaches with decision rules calibrated by simulation.
4. (a) Request or session level is acceptable if there are no carry-over effects, but user level is safer. (b) User level: memory accumulates per user, so request-level splits contaminate. (c) User or account level, often cluster or geo randomization to avoid users comparing prices; watch for network effects.
5. Primary: a decision metric tied to value (e.g. successful sessions per user, or task completion). Guardrails that can veto: latency p95, cost per user, safety reports, complaint and churn rate, regressions on critical slices. Diagnostics: thumbs-up rate, answer length, refusal rate, tool-use rate. Pre-register MDE, duration and decision rules before the launch.
