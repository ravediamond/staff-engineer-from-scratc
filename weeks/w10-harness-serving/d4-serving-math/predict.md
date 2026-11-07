# Predict

1. Llama-3-8B config (32 layers, 8 KV heads, head_dim 128, bf16). KV per token? For a 32k context?
   Guess:

2. 80 GB GPU, 16 GB of weights, 2k-token sequences on average. Max concurrent sequences?
   Guess:

3. Requests with output lengths [10, 10, 10, 500] in one static batch. When do the three short ones free their slots?
   Guess:

## Misses
-
