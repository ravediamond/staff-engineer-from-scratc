# Questions

1. Derive 16 bytes per parameter for mixed-precision Adam.
2. ZeRO-1, 2, 3: what is sharded, and what is the communication cost of each vs DDP?
3. What dominates memory besides model states, and how do you reduce it?
4. FSDP vs tensor parallelism vs pipeline parallelism: when each? How do they combine (3D parallelism)?
5. Plan memory for fine-tuning a 70B model with LoRA on 8 × 80 GB GPUs.

## Model answers

1. bf16 parameters (2) + bf16 gradients (2) + fp32 master weights for exact updates (4) + Adam m (4) + Adam v (4) = 16 bytes per parameter, before activations, buffers and fragmentation.
2. ZeRO-1 shards optimizer states (master + m + v): the same communication as DDP (2Ψ per step via reduce-scatter + all-gather). ZeRO-2 also shards gradients: still about 2Ψ. ZeRO-3/FSDP also shards parameters: about 3Ψ (all-gather params in forward and backward, reduce-scatter grads), 1.5× DDP, overlapped with compute through prefetching.
3. Activations, which scale with batch × sequence × hidden × layers. Reduce with activation checkpointing (recompute in backward), smaller micro-batches with gradient accumulation, sequence or context parallelism for long sequences, FlashAttention (no materialized attention matrix), and offloading.
4. FSDP/ZeRO: when the model fits per layer and you want simple data parallelism; scales well within and across nodes. Tensor parallelism: splits each layer's matmuls, needs very fast interconnect (within a node over NVLink); for huge layers and lower per-GPU memory. Pipeline: splits layers into stages across nodes, needs micro-batching to limit bubbles. 3D parallelism: TP within a node × PP across nodes × DP/FSDP across replicas.
5. Base weights frozen in bf16: 140 GB, sharded over 8 GPUs = 17.5 GB each (FSDP or TP), or ~35 GB total with 4-bit QLoRA. LoRA adapters (~0.1–1% of parameters) with fp32 Adam: under 1 GB. No gradients for the base. Activations dominate: use checkpointing, sequence length 4–8k, micro-batch 1–2. Comfortably fits; the bottleneck is throughput, not memory.
