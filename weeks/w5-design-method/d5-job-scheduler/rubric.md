# Rubric (grade yourself after the timer, honestly)

Score each line 0 (missing), 1 (mentioned), 2 (concrete with numbers or mechanism).

| # | Criterion | Senior signal (1) | Staff signal (2) |
|---|---|---|---|
| 1 | Requirements | lists features | separates job classes by shape, states SLOs per class, explicit non-goals |
| 2 | Estimation | some numbers | jobs/s, GPU-hours/day per class, utilisation target, $ of idle GPUs |
| 3 | API / data model | submit/status | job spec with resources, priority class, preemptible flag, idempotency, quota objects |
| 4 | Queueing core | a queue | leases + tokens, retries + DLQ, priorities, delayed jobs |
| 5 | Fairness | "per-team quota" | guaranteed quota + borrowing of idle capacity + reclaim by preemption; DRF or weighted fair share; a fairness metric |
| 6 | Gang scheduling | not addressed | all-or-nothing allocation, reservation/backfill so large jobs do not starve, topology-aware placement |
| 7 | Failure handling | "retry" | node failure → job restart from checkpoint, checkpoint contract, health checks, bad-node quarantine |
| 8 | Preemption | not addressed | grace period + SIGTERM checkpoint contract, priority classes, max preemptions per job |
| 9 | Observability | "dashboards" | utilisation, queue wait p50/p95 per class and team, goodput, preemption rate, cost per team |
| 10 | Trade-offs and scope | none | build vs buy (Kubernetes + Kueue/Volcano, Slurm, Ray), what not to build, rollout plan |

**Reading the score:** 0–9 senior or below · 10–14 senior+ · 15–17 staff · 18–20 strong staff.
The one line to improve next time:
