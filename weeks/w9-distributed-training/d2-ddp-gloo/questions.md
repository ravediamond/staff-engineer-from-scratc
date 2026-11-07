# Questions

1. Why must DDP divide the summed gradient by world size? When would it NOT be exactly equivalent to single-process?
2. Gradient accumulation + DDP: what goes wrong if you are careless, and what does `no_sync()` do?
3. Global batch 2,048 on 8 GPUs, now you move to 64 GPUs. What do you change, and what do you watch?
4. How do you test distributed training code for correctness without a cluster?
5. A run at 256 GPUs has a worse loss curve than at 32 GPUs with the same global batch. Hypotheses?

## Model answers

1. Each rank computes the mean over its local batch; the global mean is the average of the local means (equal local batch sizes), so SUM then divide by W. It is not exactly equivalent with unequal local batches (last batch), batch-norm statistics (per-rank unless SyncBN), per-rank dropout RNG streams (statistically fine, not bitwise), or floating-point reduction order.
2. Without care, gradients are all-reduced on every micro-step (wasted communication) or scaled twice (dividing the loss by accumulation steps and again by world size incorrectly). `no_sync()` skips the all-reduce on intermediate micro-steps, so gradients accumulate locally and sync once on the last micro-step. The loss must be divided by the number of accumulation steps.
3. Keep the global batch (2,048) and halve the local batch per GPU, or scale the global batch with LR scaling (linear or sqrt) and warmup, watching for generalization changes. Watch throughput (communication share grows), loss-curve equivalence on a short run, stragglers, and data-loader throughput per GPU.
4. CPU gloo equivalence tests: N processes vs 1 on the global batch for a few steps (bitwise or tight tolerance), resume equivalence, checkpoint round-trip, sharding coverage (every sample once per epoch). Run them in CI, plus small-scale GPU smoke tests.
5. Different effective hyperparameters (per-GPU batch too small for BN, LR warmup tuned for fewer steps), data sharding bugs (duplicates or skipped samples), non-determinism or reduction precision (bf16 all-reduce), stragglers causing gradient staleness (if async), different data order or seeds, or numerical issues in loss scaling. Compare curves on identical data order and check sampler coverage first.
