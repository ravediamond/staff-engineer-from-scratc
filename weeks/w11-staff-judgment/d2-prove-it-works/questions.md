# Questions

1. What does "prove it works" mean to you, concretely, for (a) a bug fix, (b) a RAG change, (c) a distributed training change?
2. Property-based vs example-based tests: when each? Name three properties for a chunker (W6 D1).
3. Why does shrinking matter so much?
4. How would you build a "verification skill" an agent must run before claiming a task done?
5. A teammate says "it works on my machine and the demo looked good". What do you ask for, without being a jerk?

## Model answers

1. (a) A failing test that reproduces the bug before the fix and passes after, plus the full suite green. (b) A paired evaluation on a labelled set with CIs and slice gates, plus a look at 20 changed answers. (c) Equivalence tests (N-process vs 1-process, resume vs no resume) and a short real run whose loss curve matches the baseline within noise.
2. Example-based for specific known cases and regressions; property-based for invariants over large input spaces (parsers, data structures, transforms). Chunker properties: spans cover the text with no gaps, every chunk ≤ max_len (unless unsplittable), concatenating chunk texts reproduces the source, offsets are monotonic.
3. A random failing input is often large and noisy; the minimal one points straight at the mechanism (e.g. "three equal values" → the duplicate-skip logic), and it makes a readable regression test.
4. A tool that takes the task's claim and runs checks matching the change type: tests touched and their before/after, linters and type checks, property tests for touched modules, evals for prompt or model changes. It outputs a structured evidence report attached to the PR; the harness refuses "done" without a passing report and records overrides.
5. "Nice. Can you add the test or the eval run that shows it, so reviewers and future us can rely on it? Here's how I usually do it for this kind of change." Offer a template or pairing. Make evidence the team norm, not a personal demand.
