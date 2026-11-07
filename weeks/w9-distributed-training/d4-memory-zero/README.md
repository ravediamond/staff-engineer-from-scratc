# W9 D4: memory math and ZeRO

Primer: `knowledge/09-distributed-training.md` §4.
Reference: Rajbhandari et al., "ZeRO: Memory Optimizations Toward Training Trillion Parameter Models" (2020).

## The one idea

Mixed-precision training with Adam keeps, **per parameter** (Ψ = number of parameters):

| State | Bytes |
|---|---|
| bf16/fp16 parameters | 2 |
| bf16/fp16 gradients | 2 |
| fp32 master parameters | 4 |
| fp32 Adam first moment m | 4 |
| fp32 Adam second moment v | 4 |
| **total** | **16 Ψ** (plus activations) |

A 7B model needs 112 GB of model states: it does not fit on one 80 GB GPU **before activations**.
ZeRO shards these states across N data-parallel ranks:

| Mode | Per-GPU bytes |
|---|---|
| DDP | 16Ψ |
| ZeRO-1 (shard optimizer states: master + m + v) | 2Ψ + 2Ψ + 12Ψ/N |
| ZeRO-2 (+ shard gradients) | 2Ψ + 14Ψ/N |
| ZeRO-3 / FSDP (+ shard parameters) | 16Ψ/N |

**ZeRO-1 in one sentence:** every rank computes the full averaged gradient, but only updates its own
shard of parameters with its own shard of optimizer state, then all-gather the updated shards. The
result must be identical to full Adam: that is today's test.

## Today's build (`w9d4_zero.py`)

`model_state_bytes(psi, mode, n)`, `max_params(gpu_gb, mode, n, reserve_gb)`,
`adam_step(p, g, m, v, t, lr, b1, b2, eps)` (manual, numpy), `zero1_step(params, grads_per_rank, states, t, ...)`.

## Staff angle

Memory math decides architecture choices before any code: "70B with FSDP on 64 × 80 GB: model states
are 16 × 70e9 / 64 = 17.5 GB per GPU, leaving ~55 GB for activations; with activation checkpointing
at sequence 8k that fits; without, it doesn't". Being able to do this in your head is what makes you
credible in a training-infra discussion.
