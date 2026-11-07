# Rubric

Score each line 0 / 1 / 2.

| # | Criterion | Senior signal (1) | Staff signal (2) |
|---|---|---|---|
| 1 | Requirements | "agent that writes code" | task types in scope, success definition (merged PR, tests pass), safety constraints, non-goals |
| 2 | Estimation | none | tasks/day, steps and tokens per task, $ per task, sandbox compute, review time budget |
| 3 | Sandbox | "docker" | isolated per-task VM/container, no ambient credentials, egress allow-list, scoped tokens, audit log |
| 4 | Harness loop | "LLM + tools" | tools with schemas, budgets, retries in executor, idempotent side effects, trace for every run |
| 5 | Verification | "run tests" | explicit verify step: tests, linters, type checks, repro of the bug before/after; refuses to claim done without evidence |
| 6 | Offline eval | "benchmark" | internal task set from historical tickets with hidden tests, SWE-bench-style harness, slices by repo/language/task type, CIs |
| 7 | Online eval | "user feedback" | PR merge rate, review time, revert rate, time-to-merge vs matched human baseline, A/B or staggered rollout |
| 8 | Cost control | none | budget per task, model routing, caching, early termination on low-confidence plans |
| 9 | Failure modes | none | test tampering, over-broad changes, flaky tests, prompt injection from repo content, secrets in logs |
| 10 | Scope / rollout | none | start with low-risk task types and opt-in teams, human approval for merges, success metric |

0–9 senior or below · 10–14 senior+ · 15–17 staff · 18–20 strong staff.
