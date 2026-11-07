# Questions

1. Why paired comparisons? Quantify the gain in one sentence.
2. How do you handle non-determinism in LLM evals?
3. Design the release gate for a team shipping prompt changes daily. Who can override it?
4. Your eval set is 18 months old. What goes wrong and how do you refresh it without breaking comparability?
5. "Eval passed, users complain." Your process?

## Model answers

1. Per-case difficulty variance cancels: the variance of the difference is var(A) + var(B) − 2cov(A,B), and with high correlation between systems (usual), the paired CI can be several times narrower, so far fewer cases detect the same effect.
2. Measure it first: repeat runs and report per-case std plus flaky cases. Then reduce it (temperature 0 where the product allows, fixed seeds, cached tool responses) or account for it (k repeats and mean per case, CI across runs). Never compare two single runs.
3. Pre-registered rule in CI: paired bootstrap on the core set; block on a significant regression or on a slice drop beyond tolerance on critical slices (safety, top customers); warn on non-significant drops. Results are posted on the PR. An override needs a named approver (eval owner or staff engineer) with a written reason, logged, and reviewed weekly.
4. It drifts from real traffic (new intents, products, languages), may leak into prompt tuning (overfit), and saturates. Refresh: keep a frozen "anchor" subset for longitudinal comparability, add new cases quarterly from production samples, version every set, report both, and re-baseline all systems on the new version before comparing.
5. Collect the complaints and turn them into cases (with labels); check whether they are a slice missing from the set, a metric that does not measure what users care about, or a distribution shift. Add the slice, fix or add the metric, re-run the gate, and track the offline-to-online agreement rate (D5).
