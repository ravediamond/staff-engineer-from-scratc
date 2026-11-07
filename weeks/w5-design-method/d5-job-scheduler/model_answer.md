# Model answer: ML job scheduler (staff level)

## 1. Requirements
Functional: submit jobs with resource specs (GPU count/type, CPU, memory), priority class, team;
query status and logs; cancel; quotas per team; preemption of lower classes.
Non-functional: queue wait p95 < 5 min for eval jobs, < 1 h for training jobs within quota;
scheduler decision < 1 s; no lost jobs (durable state); GPU allocation (fraction of GPU-hours
allocated to running jobs) > 85%, goodput (useful training progress) > 75%.
Non-goals: a new cluster manager from scratch, cross-region scheduling, cost chargeback billing (v2).

## 2. Estimation
50k jobs/day ≈ 0.6 jobs/s average, ~5/s peak: scheduling throughput is not the problem.
Capacity: 2,000 GPUs × 24 h = 48k GPU-hours/day. Rough mix: eval 40k jobs × 0.2 h = 8k GPU-h;
batch 8k jobs × 2 h × 2 GPUs = 32k GPU-h; fine-tune 50 jobs × 16 h × 16 GPUs ≈ 13k GPU-h.
Demand ≈ capacity, so fairness and packing matter. 10% idle at $2/GPU-h ≈ $96k/month: that is the
business case.

## 3. API and data model
`POST /jobs {spec, team, class: [prod, standard, preemptible], idempotency_key}` → job id.
Job record: id, team, class, resources, state, attempts, lease token, checkpoint URI, timestamps.
Quota: team → guaranteed GPUs per type, borrow limit. Node: GPUs, health, topology (rack, NVLink domain).

## 4. Architecture
Build on Kubernetes plus a batch scheduler (Kueue or Volcano); write our policy layer, not a
cluster manager. Components: API → durable job store (Postgres) → admission controller (quota
check, cohort borrowing) → placement (gang, topology-aware) → node agents. Workers report
heartbeats; the controller reaps lost leases. Request: submit → validated and stored → admitted
when quota allows (or borrows idle capacity as preemptible) → placed all-or-nothing → running →
checkpoints to object storage → done; metrics emitted at each transition.

## 5. Deep dives
**Fairness:** each team has a guaranteed share. Idle capacity can be borrowed, but borrowed pods
are preemptible and reclaimed when the owner needs them. Order within the queue by weighted fair
share of recent usage (DRF across GPU + memory). Metric: per team, (GPU-hours received) / (min(demand,
share)) over 7 days, plus queue wait percentiles per team.
**Gang scheduling and starvation:** allocation is all-or-nothing; large jobs get a reservation
once they reach the head of their class queue, and small jobs backfill into the reserved nodes
only if they finish before the reservation's expected start (based on declared max runtime).
Topology: place gangs within one NVLink/InfiniBand domain to keep all-reduce fast.
**Failure and preemption contract:** jobs must handle SIGTERM by checkpointing within 120 s;
the platform guarantees the grace period and restarts the job from the latest manifest-referenced
checkpoint (fenced by generation number, W3 D5). Nodes failing health checks twice are
quarantined. Max 3 preemptions per job per day, then it gets protected status.

## 6. Metrics, risks, scope
Metrics: allocation and goodput, queue wait p50/p95 per class and team, preemptions per job,
lost GPU-hours to failures, cost per team. Risks: teams gaming priority classes (charge more for
prod class), checkpoint storage cost, stragglers in gangs. Not built: our own placement engine,
cross-region, spot-market bidding. Rollout: shadow mode (compute decisions, compare with the
spreadsheet), then one team, then all.
