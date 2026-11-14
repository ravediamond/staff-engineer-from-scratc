# Model answer: host and fine-tune LLMs on Kubernetes

**Clarify.** Mostly chat and RAG: ~1,500 input and ~300 output tokens per request. Interactive SLO:
TTFT p95 < 500 ms, inter-token p95 < 50 ms; batch traffic has none. Tenants = 40 applications with
budgets. Fine-tuning: LoRA for 15 teams, full fine-tuning of the 8B for a few. EU only. Non-goals for
v1: multi-region active-active, training from scratch, serving arbitrary user-supplied models.

**Numbers (derived, to be benchmarked).**
- Weights in bf16: 8B = 16 GB, 32B = 64 GB, 70B = 140 GB (4 × 80 GB GPUs with tensor parallelism, or
  2 with 8-bit weights).
- KV cache: 8B ≈ 128 KiB/token → 1 GiB per 8k sequence → ~60 sequences on an 80 GB GPU. 70B ≈ 320 KiB/token.
- 8B: 300 req/s × 300 output tokens = 90k tokens/s. If one GPU gives ~2.5–3k tokens/s at this latency,
  that is ~32–36 GPUs: too much of the budget, so quantise (FP8/AWQ), cap output, cache, and route
  simple traffic to it only; plan ~24 GPUs with autoscaling. 32B: ~8 GPUs. 70B: 20 req/s × 300 = 6k
  tokens/s → 3–4 replicas of 4 GPUs = 12–16 GPUs.
- Serving ≈ 44–48 reserved GPUs at peak, leaving ~16 reserved plus night-time borrowed capacity and spot for fine-tuning.
- Full fine-tune of 8B: ~16 bytes/param with mixed-precision Adam ≈ 128 GB + activations → 4 GPUs with
  FSDP. LoRA/QLoRA of the 32B: one GPU.

**Architecture.**
```
clients -> API gateway (OIDC, tenant, token-bucket quotas in TOKENS, audit)
        -> inference gateway (Gateway API + Inference Extension: InferencePool, endpoint picker
           scoring queue depth, KV usage, prefix-cache and LoRA affinity, priority)
        -> vLLM pools: 8B and 32B as Deployments (KServe LLMInferenceService), 70B as LeaderWorkerSet
           replicas; tainted GPU node pools; node-local weight cache
fine-tune: API/CLI -> TrainJob template (Kubeflow Trainer on JobSet) -> Kueue (ClusterQueue per team,
           cohort with borrowing, preemption, gang admission) -> spot pool -> sharded checkpoints in
           object storage -> eval gate (W7 harness) -> model/adapter registry with lineage -> canary
platform:  GPU Operator (driver, device plugin or DRA driver, MIG manager, DCGM exporter), node
           autoscaler with reservations, Prometheus + OpenTelemetry, Argo CD, RBAC, NetworkPolicy, KMS
```

**Request path.** TLS ends at the gateway; the tenant is resolved and its token budget checked; the
endpoint picker chooses a replica with the prompt prefix cached and the adapter loaded and a short
queue; vLLM batches continuously with paged KV; tokens stream back over SSE; tokens are metered per
tenant and traced (queue time, TTFT, TPOT).

**GPU scheduling.** Serving runs on reserved nodes with a high PriorityClass. Training runs on spot
plus whatever reserved capacity serving is not using, through Kueue borrowing; serving reclaims by
preemption. Bin-packing on GPU pools keeps whole nodes for multi-GPU jobs. Small models and notebooks
get MIG slices. DRA for new clusters where the driver supports it, device plugin otherwise. Jobs are
admitted all-or-nothing, in one network domain when topology matters.

**Autoscaling.** Never on GPU utilisation. KEDA/HPA on requests waiting per replica and KV usage, with
TTFT p95 as the guardrail. Replicas take minutes to arrive (node + image + weights + load), so: minimum
replicas sized for the daily base, 30% headroom, pre-pulled images, weights cached on node NVMe,
scale-down stabilised. During a 5× spike: priority queues, batch traffic shed first, then 429 with
Retry-After per tenant quota; the large model degrades to the 32B for tenants that allow it.
Scale-to-zero only for rarely used internal models.

**Fine-tuning lifecycle.** Dataset version with PII scrub and licence check → TrainJob from a
template (base model pinned, LoRA rank and targets, seed) → Kueue admission → checkpoints every
sqrt(2 × cost × MTBF) (about 30 min for a 2-min checkpoint on spot) with automatic resume → frozen
eval suite plus safety regressions → registry entry (data hash, code SHA, base, metrics) → canary at
5% with online guardrails → served as a dynamically loaded adapter on the shared base (hot tenants:
merged weights on dedicated replicas).

**Failure modes.** GPU Xid/ECC: DCGM health → cordon, drain, replace; jobs resume from checkpoint.
Hung collective or straggler: step-time watchdog restarts the gang. KV OOM: context caps and admission
by KV usage. Long prefills starving decodes: chunked prefill, separate pools for long-context traffic.
Spot reclaim: checkpoint + requeue; head pod on on-demand. Adapter thrash: affinity routing and a
bounded hot set. Rollout with no spare GPUs: maxSurge 0 / maxUnavailable 1 with graceful drain, at low
traffic. Region outage: v1 accepts RTO of hours from infrastructure-as-code and replicated artefacts;
warm standby is phase 2.

**Cost.** $/1M output tokens = $/GPU-hour ÷ (tokens/s × 3600) × 10⁶ ÷ utilisation: at $3/h and 2,000
tokens/s, $0.42 at full load, $2 at 20%. Levers in order: utilisation (consolidate models, batch
traffic at night on the same GPUs), quantisation and prefix caching, routing easy requests to the
small model. Showback per tenant from metered tokens.

**Build vs buy.** Buy: the long tail of models through a managed EU endpoint; the cluster itself
(managed Kubernetes). Build: the gateway policy, the eval gate and the fine-tuning templates: that is
where the company-specific value is. Revisit self-hosting each model when its monthly bill crosses the
cost of two dedicated GPUs.
