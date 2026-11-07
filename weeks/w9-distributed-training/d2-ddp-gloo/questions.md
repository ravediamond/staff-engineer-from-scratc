# Questions

1. Why must DDP divide the summed gradient by world size? When would it NOT be exactly equivalent to single-process?
2. Gradient accumulation + DDP: what goes wrong if you are careless, and what does `no_sync()` do?
3. Global batch 2,048 on 8 GPUs, now you move to 64 GPUs. What do you change, and what do you watch?
4. How do you test distributed training code for correctness without a cluster?
5. A run at 256 GPUs has a worse loss curve than at 32 GPUs with the same global batch. Hypotheses?

