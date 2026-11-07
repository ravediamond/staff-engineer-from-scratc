# 09. Distributed training

## §1 Collectives

All-reduce = reduce-scatter + all-gather; ring sends 2(N−1)/N of the buffer per worker. Tree/hierarchical for small
messages and many nodes. NCCL picks by size and topology. Overlap communication with backward (buckets).

## §2 Data parallelism

All-reduce SUM then divide by world size (equal local batches). Distributed sampler: same seed + epoch on every rank,
padded, strided. Gradient accumulation with `no_sync()`. Equivalence tests: N processes == 1 process.

## §3 Resume

Save model, optimizer, scheduler, scaler, step, all RNGs, data position, metadata; atomic writes; restore RNG last.
Checkpoint interval ≈ √(2 · cost · MTBF) (Young/Daly).

## §4 Memory and sharding

Mixed-precision Adam: 16 bytes/parameter of model states. ZeRO-1/2/3 shard optimizer states, gradients, parameters
(FSDP ≈ ZeRO-3). Activations: checkpointing, micro-batching, sequence/context parallelism, FlashAttention.
Tensor parallelism within a node (NVLink), pipeline across nodes (bubbles shrink with more micro-batches),
FSDP/DP across replicas: 3D parallelism.

## §5 Checkpoints, efficiency, reliability

Sharded checkpoints with a manifest written last and checksums; async upload; resharding for elastic restarts.
MFU = 6·P·tokens/s / (GPUs · peak). Goodput = useful progress / paid time. Large clusters fail every few hours:
detection, quarantine, spares, automatic restart.

## Numbers

| Thing | Value |
|---|---|
| FLOPs per token, training (dense) | ≈ 6 × parameters |
| Training compute | ≈ 6 × parameters × tokens (Chinchilla-optimal tokens ≈ 20 × parameters) |
| Model states, mixed-precision Adam | 16 bytes × parameters |
| Good MFU, large dense models | 40–55% |
| H100 NVLink (per GPU, per direction) | ~450 GB/s |
| InfiniBand NDR per port | 400 Gb/s ≈ 50 GB/s |

## Questions

1. Estimate the time to train a 7B model on 1T tokens with 256 H100s at 45% MFU.
<details><summary>Answer</summary>Compute = 6 × 7e9 × 1e12 = 4.2e22 FLOPs. Throughput = 256 × 990e12 × 0.45 ≈ 1.14e17 FLOP/s. Time ≈ 3.7e5 s ≈ 4.3 days, plus overheads for failures and evals (say a week).</details>

2. Loss spikes mid-run. Your playbook?
<details><summary>Answer</summary>Check for bad data batches (log batch ids; skip the offending range), LR too high for the current phase, numerical issues (bf16 overflow, attention logit growth: use QK-norm or z-loss), and hardware (silent data corruption: compare across DP replicas). Roll back to a checkpoint before the spike, skip the data window, optionally lower LR, and resume. Add monitoring for gradient norm and per-layer activation scales.</details>

3. FSDP vs DeepSpeed ZeRO vs Megatron-style TP/PP: how do you choose for a 13B fine-tune on 16 GPUs?
<details><summary>Answer</summary>FSDP (or ZeRO-3) across 2 nodes is simplest and sufficient: model states 16 × 13e9 / 16 = 13 GB per GPU, activation checkpointing for long sequences. TP/PP add complexity worth it only when a single layer or the activations do not fit, or at much larger scale. Prefer the stack the team already operates.</details>
