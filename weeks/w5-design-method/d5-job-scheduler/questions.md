# Questions

1. Why lease tokens and not just job ids on completion?
2. Retries vs DLQ: what goes to the DLQ and who looks at it?
3. Explain gang scheduling and the starvation problem it creates. How does backfill help?
4. How do you make GPU sharing fair across 12 teams? What metric proves it?
5. Kubernetes + Kueue, Slurm, Ray, or build: how do you decide?

## Model answers

1. After a lease expires, the same job id is held by a new worker. Only a per-lease token tells the current holder from a zombie, so stale completions (duplicate or overwriting results) are rejected.
2. Jobs that failed max_attempts times or are invalid (poison inputs, bad configs). An owner team is paged, or gets a ticket above a threshold. DLQ items keep their full context (spec, logs, last error) and can be replayed after a fix. The DLQ size is itself an alert.
3. A multi-node job needs all N GPUs simultaneously. If small jobs keep grabbing freed GPUs, the large job never sees N free at once. Reserve capacity for the head-of-line large job, and let small jobs backfill the reserved nodes only if their declared runtime ends before the reservation starts.
4. Guaranteed quotas, borrowing of idle capacity as preemptible, reclaim on demand, and ordering by weighted fair share (DRF for multi-resource). Metric: delivered GPU-hours relative to min(demand, entitled share) per team over a window, plus queue-wait percentiles per team. Review it monthly with the teams.
5. Most companies on Kubernetes should use Kueue/Volcano for quota and gangs. Slurm if the users are HPC/research people running long multi-node jobs on bare metal. Ray when the workload is Python-native distributed apps (data + training + serving) and teams want one framework. Build only the policy layer. Decide on users' workflow, existing infrastructure, the multi-node needs and the team's operational capacity.
