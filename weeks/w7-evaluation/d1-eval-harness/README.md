# W7 D1: eval harness, flakiness, slices, regression gates

Primer: `knowledge/07-evaluation-and-experimentation.md` §1–2.

## The one idea

An eval harness is a measurement instrument. Like any instrument it needs: a fixed input set,
known noise, a resolution (smallest change it can detect), and a decision rule.

- **Repeats** expose non-determinism (sampling temperature, tool flakiness). A case whose score
  varies across repeats is **flaky**: report it, do not average it away silently.
- **Slices** (language, intent, customer, difficulty) catch regressions that the global mean hides.
- **Paired comparison:** both systems run on the **same cases**, so compare per-case differences.
  Case difficulty varies far more than the system effect; pairing cancels it. The paired bootstrap
  resamples **case indices** and recomputes the mean difference.
- **Gate:** a pre-registered rule, decided before seeing results. Today: fail if the paired CI
  shows a significant regression (upper bound < 0), if the mean drops by more than a tolerance, or
  if any slice drops by more than its tolerance.

## Today's build (`w7d1_harness.py`)

`run_eval(cases, system, metric, repeats)` → `{case_id: (mean, std)}`, `flaky(results, tol)`,
`slice_means(scores, cases)`, `paired_bootstrap(base, new, n_boot, seed)` → `(delta, lo, hi)`,
`gate(base, new, cases, max_drop, slice_max_drop, n_boot, seed)` → `{"pass": bool, "reasons": [...]}`.

## Staff angle

The staff contribution to evaluation is **governance**, not code: who owns the eval set, how it
is refreshed without leaking into training/prompt tuning, which gate blocks a release and who can
override it, how "eval passed but users complain" feeds back into new cases. Write that down
once, and thirty teams ship faster because they stop arguing about whether a change is better.
