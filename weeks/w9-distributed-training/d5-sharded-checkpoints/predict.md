# Predict

1. 7B model, 1,000 GPUs at 990 TFLOP/s peak (bf16 dense), 2.5M tokens/s. MFU?
   Guess:

2. A job fails every 4 hours, checkpoints every hour, restart takes 15 minutes. Goodput lost to failures?
   Guess:

3. Rank 0 writes the manifest first, then node 3 dies before writing its shard. What does a naive loader do?
   Guess:

## Misses
-
