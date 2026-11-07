# Model answer: multi-node training platform (staff level)

## 1. Requirements
Workloads: pretraining/continued pretraining up to 70B (weeks, 256–512 GPUs), fine-tuning 1–70B
(hours–days, 8–64 GPUs), evals (W5 scheduler). Goodput target > 85% for large runs. Reproducible runs
(config + code + data version, deterministic data order). Multi-tenant with quotas. Non-goals: custom
kernels team, serving (separate), cross-cluster training.

## 2. Estimation
Failures: large-scale reports (e.g. Meta's Llama 3 training) show roughly one interruption every ~3
hours at 16k GPUs; scaled to 512 GPUs, expect on the order of one per day or two, mostly GPU/HBM, NIC
and host issues. A 3-week 70B run will be interrupted ~10–20 times. Checkpoint 70B: 16 × 70e9 ≈ 1.1 TB
of model + optimizer state. Write to local NVMe at ~5 GB/s per node × 64 nodes = 320 GB/s → ~4 s
snapshot, upload async to object storage (~25 GB/s aggregate → ~45 s). Young/Daly with 4 s blocking
cost and a 24 h MTBF → checkpoint every ~10 min (blocking cost is tiny). Data: 512 GPUs × ~3k tokens/s
(70B) ≈ 1.5M tokens/s ≈ 6 MB/s pre-tokenized: trivial throughput, latency and determinism matter more.

## 3. Architecture
Slurm (or K8s + Kueue) for gang scheduling with topology-aware placement (whole nodes, same IB leaf
switch for TP/PP groups). Training framework: standard recipes on torchtitan / Megatron-style with
FSDP2, TP, PP, activation checkpointing, async distributed checkpointing. Data: pre-tokenized,
sharded, versioned datasets on object storage + node-local cache; sampler state is part of the
checkpoint. Control plane: job controller watching heartbeats and NCCL timeouts, health service
(DCGM checks, burn-in tests on new or repaired nodes), spare pool (2–4 nodes). Tracking: every run
records config hash, git SHA, dataset version, cluster topology; checkpoints carry the same metadata
and link to eval runs.

## 4. Deep dives
**Failure recovery:** detection (NCCL timeout, missing heartbeat, ECC errors) → job controller kills
the job, quarantines suspected nodes (diagnostics decide return-to-pool), swaps in spares, restarts
from latest complete checkpoint (manifest + checksums) within ~10 min. If spares run out, elastic
restart with fewer DP replicas (resharding FSDP state, adjusted gradient accumulation to keep global
batch). Track lost GPU-hours per incident class.
**Parallelism recipes and MFU:** ≤13B: FSDP across nodes, TP not needed; 70B: TP=8 within node over
NVLink, PP=2–4 across nodes or FSDP across, sequence parallel for long contexts. Each recipe has a
reference MFU (40–50%) on the cluster, a regression test, and a performance dashboard; jobs below
70% of their recipe's MFU get flagged (stragglers, bad data loader, misconfig).

## 5. Metrics, risks, scope
Cluster: allocation, goodput per job, MFU per job, interruptions/day by cause, mean time to recover,
checkpoint time, queue wait by class, cost per team. Risks: silent data corruption (periodic
checksums of parameters across DP replicas), loss spikes (automatic rollback to the previous
checkpoint with data skip), storage costs (retention policy: keep every Nth checkpoint). Rollout: burn
in hardware for 2 weeks, one flagship run with the platform team embedded, then open to all.
