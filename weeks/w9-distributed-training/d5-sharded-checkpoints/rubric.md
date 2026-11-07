# Rubric

Score each line 0 / 1 / 2.

| # | Criterion | Senior signal (1) | Staff signal (2) |
|---|---|---|---|
| 1 | Requirements | "run training" | job types and sizes, goodput target, reproducibility, multi-tenancy, non-goals |
| 2 | Estimation | none | failure rate at 512 GPUs, checkpoint size (16Ψ for 70B ≈ 1.1 TB), write bandwidth, tokens/s needed |
| 3 | Scheduling | "a queue" | gang scheduling, topology-aware placement, quotas, preemption contract (reuses W5) |
| 4 | Parallelism | "use FSDP" | strategy per model size (FSDP for ≤13B, TP within node + PP/FSDP across for 70B), standard recipes, MFU targets |
| 5 | Checkpointing | "save every N steps" | sharded, async to local NVMe then object storage, manifest last, frequency from Young/Daly, integrity checks |
| 6 | Failure recovery | "restart" | health checks, node quarantine, hot spares, automatic restart from latest complete checkpoint, elastic resharding |
| 7 | Data pipeline | "dataloader" | pre-tokenized sharded datasets, deterministic sampling with resumable state, throughput headroom, data versioning |
| 8 | Observability | "dashboards" | MFU, goodput, step time breakdown, straggler detection, loss-spike alerts, per-job cost |
| 9 | Experiment tracking | none | config + code + data version per run, lineage from checkpoint to eval results |
| 10 | Scope / rollout | none | buy vs build (Slurm/K8s + torchtitan/Megatron, W&B/MLflow), pilot with one team, success metric |

0–9 senior or below · 10–14 senior+ · 15–17 staff · 18–20 strong staff.
