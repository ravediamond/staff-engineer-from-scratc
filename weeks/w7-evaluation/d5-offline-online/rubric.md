# Rubric

Score each line 0 / 1 / 2.

| # | Criterion | Senior signal (1) | Staff signal (2) |
|---|---|---|---|
| 1 | Requirements | "run evals" | gate latency target (e.g. < 30 min per PR), coverage of slices/markets, reproducibility, non-goals |
| 2 | Estimation | none | cases × repeats × changes/week → model calls → $ per week; judge cost; budget per team |
| 3 | Data model | "datasets" | versioned datasets, cases with slices and provenance, runs tied to code/prompt/model hashes, immutable results |
| 4 | Execution | "a script" | distributed runner, caching of unchanged components, repeats for non-determinism, tool mocking or recorded fixtures |
| 5 | Statistics | averages | paired bootstrap, slice gates with multiple-comparison control, MDE known per dataset |
| 6 | Judges | "use GPT-4" | calibration set with human κ, judge κ reported, position/verbosity controls, recalibration on change |
| 7 | Online | none | A/B platform integration, SRM checks, guardrails (latency, cost, safety), offline↔online agreement tracking |
| 8 | Governance | none | dataset owners, refresh cadence, override process, eval review meeting, incident → new cases loop |
| 9 | Developer experience | none | results on the PR in minutes, local quick-eval, clear diff views of failing cases |
| 10 | Scope / rollout | none | start with top 3 teams and core datasets, shadow gates before blocking, success metric (regressions reaching users) |

0–9 senior or below · 10–14 senior+ · 15–17 staff · 18–20 strong staff.
