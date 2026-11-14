# 18. ML platform on Kubernetes: GPUs, training, LLM serving

Week 14, days 4–5. Read after `09` (distributed training) and `11` (LLM serving). Project versions move
monthly: check the project pages before quoting a version in an interview.

## 1. Getting GPUs into pods

- **NVIDIA GPU Operator** installs the driver, container toolkit, **device plugin** (or the DRA
  driver), MIG manager, node feature discovery and the **DCGM exporter** (utilisation, memory, power,
  temperature, Xid errors).
- Device plugin: `resources.limits: nvidia.com/gpu: 1`: a counter of whole, interchangeable GPUs.
- **DRA** (Dynamic Resource Allocation, `resource.k8s.io`, GA in Kubernetes 1.34, August 2025):
  `DeviceClass`, `ResourceClaim(Template)`, `ResourceSlice`; select devices by attributes with CEL
  ("memory ≥ 40Gi"), share a claim between containers, express constraints between devices.
- Dedicated pools: taint GPU nodes, tolerate + select from GPU workloads, bin-pack.
- Sharing: **MIG** (hardware isolation, fixed profiles), **MPS** (concurrent, weak isolation),
  **time-slicing** (no memory isolation).

## 2. Batch: queues, quotas, gangs

- **Gang scheduling**: all pods of a job or none. **Kueue** (admission: ResourceFlavor, ClusterQueue,
  LocalQueue, cohorts with borrowing and reclaim, priorities, fair sharing, topology-aware
  scheduling), or Volcano / YuniKorn / KAI Scheduler (batch schedulers with pod groups).
- Job APIs: **Kubeflow Trainer v2** `TrainJob` + `TrainingRuntime` on **JobSet** (replaces the
  per-framework `PyTorchJob`, `TFJob`, `MPIJob` of the old Training Operator); **KubeRay** for Ray
  workloads; plain indexed `Job` for embarrassingly parallel work.
- Spot: checkpoint every `sqrt(2 × checkpoint cost × MTBF)`, resume automatically, keep the
  coordinator on on-demand capacity.
- Data and checkpoints: object storage as the source of truth; local NVMe as cache; FUSE mounts or
  streaming loaders for datasets; sharded checkpoints with a manifest (W9 D5).

## 3. Why utilisation is low and people still wait

Fragmentation, static quotas, partial gangs, idle interactive sessions, one small model per GPU,
input-pipeline-bound training. Know the mechanism that fixes each (W14 D4 questions).

## 4. Serving LLMs

- Engine: **vLLM** (continuous batching, paged KV cache, prefix caching, multi-LoRA), TGI, Triton
  with TensorRT-LLM, SGLang. Math from `11`: weights = 2 bytes/param in bf16; KV per token =
  `2 × layers × kv_heads × head_dim × bytes`; memory caps concurrency.
- Kubernetes layer: **KServe** (`InferenceService`; `LLMInferenceService` for LLMs), the vLLM
  production-stack Helm chart, **LeaderWorkerSet** for models spanning nodes, **llm-d** for
  disaggregated prefill/decode and cache-aware scheduling.
- Routing: **Gateway API Inference Extension** (`InferencePool`, endpoint picker): choose the
  replica by queue depth, KV-cache usage, prefix-cache and adapter affinity, request priority.
- Autoscaling: on waiting requests, KV usage or TTFT through KEDA/HPA. Never on GPU utilisation.
  Headroom and warm replicas, because cold start = node + image + weights + load (minutes).
- Rollouts without spare GPUs: `maxSurge 0 / maxUnavailable 1`, startup probes, graceful drain of streams.
- Multi-tenancy: quotas in tokens, priority classes, per-tenant metering, adapters per tenant.

## 5. Fine-tuning as a product

Dataset version (PII, licence) → job template (LoRA / QLoRA / full; base pinned) → quota and gang
admission → checkpoints → **eval gate** (W7) → **registry** with lineage (data hash, code SHA, base
model, metrics) → canary → serve as adapter on a shared base, or merged for hot tenants.
LoRA: `W' = W + (α/r)·B·A`, trainable params `r·(d_in + d_out)` per adapted matrix, B starts at zero.
QLoRA: 4-bit NF4 base + double quantisation + paged optimizer: a 65B model on one 48 GB GPU.
Full fine-tuning memory: ~16 bytes/param with mixed-precision Adam (weights, gradients, two moments).

## 6. Numbers and SLOs to say out loud

TTFT p95 and inter-token latency for interactive traffic; tokens/s per GPU from a benchmark, not a
blog; $/1M tokens = $/GPU-h ÷ (tokens/s × 3600 × utilisation) × 10⁶; MFU and goodput for training;
GPU-hours per team for showback.

## 7. Failure modes worth volunteering

GPU Xid/ECC errors (cordon and replace), hung collectives, KV out-of-memory, long prefills starving
decodes, spot reclaim storms, adapter thrash, image or weight pulls dominating scale-up, driver
upgrades (roll node pools with PDBs), a noisy tenant without token budgets.

## Questions

1. What can a ResourceClaim say that `nvidia.com/gpu: 1` cannot?
<details><summary>Answer</summary>Which device: by model, memory, topology; several devices with constraints; shared between containers; partitionable devices.</details>

2. What does Kueue decide, and what does it leave to others?
<details><summary>Answer</summary>When a workload may start and against which quota/flavor (admission, borrowing, preemption). Placement stays with the scheduler, nodes with the autoscaler.</details>

3. Why is round-robin wrong for LLM replicas?
<details><summary>Answer</summary>Replicas differ by queue, KV pressure, cached prefixes and loaded adapters; ignoring that costs latency and throughput.</details>

4. Give the cold-start budget of a 70B replica.
<details><summary>Answer</summary>Node 2–5 min + image 10+ GB + 140 GB of weights + load to GPU: several minutes. Mitigate with warm capacity, pre-pulled images, node-local weight cache.</details>

5. Merged weights or dynamic adapters?
<details><summary>Answer</summary>Dynamic adapters for many low-traffic tenants on a shared base; merged weights on dedicated replicas for the few hot ones.</details>
