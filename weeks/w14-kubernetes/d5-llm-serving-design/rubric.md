# Rubric

Score each line 0 / 1 / 2.

| # | Criterion | Senior signal (1) | Staff signal (2) |
|---|---|---|---|
| 1 | Requirements | models and QPS restated | token mix per request, interactive vs batch, SLOs (TTFT, inter-token), tenants, residency, who fine-tunes and how, non-goals |
| 2 | Estimation | "N GPUs per model" | weights and KV per token derived, concurrency per GPU, tokens/s → replicas per model with headroom, training memory (full vs LoRA), fits the 64-GPU budget explicitly |
| 3 | Serving stack | "vLLM pods behind a Service" | gateway with auth and token quotas → inference-aware routing (queue, KV, prefix, adapter) → vLLM pools; multi-node for the 70B; streaming; graceful drain |
| 4 | Autoscaling | HPA on CPU/GPU | queue depth / KV usage / TTFT via custom metrics; headroom and warm replicas because of cold start; priority and load shedding; scale-to-zero only where acceptable |
| 5 | GPU scheduling | "GPU node pool" | taints + selectors, device plugin vs DRA, MIG for small models, bin-packing, serving on reserved capacity and training on spot, driver upgrades in waves |
| 6 | Multi-tenancy & quotas | namespaces | Kueue-style quotas with borrowing and reclaim, gang admission, priorities (serving > interactive > batch), fair sharing, showback per team |
| 7 | Fine-tuning lifecycle | "run a training job" | versioned data with PII checks → templated job (LoRA/QLoRA/full) → gang-admitted → checkpoints to object storage (interval justified) → eval gate → registry with lineage → canary → multi-LoRA or merged serving |
| 8 | Failure modes | pod restarts | GPU faults (Xid, DCGM, cordon), hung collectives, KV OOM, long prefills, spot reclaim, adapter thrash, rollout without spare GPUs, region loss with a stated RPO/RTO |
| 9 | Observability & cost | dashboards | TTFT/TPOT histograms, queue, KV usage, prefix-hit rate, tokens per tenant, GPU health, MFU and goodput for training; $/1M tokens per model and the levers |
| 10 | Judgment | builds everything | build vs buy stated (managed endpoints for the long tail), v1 scope, migration path, security (RBAC, network policy, safetensors, signed images), what would change at 10× |

0–9 senior or below · 10–14 senior+ · 15–17 staff · 18–20 strong staff.
