# Predict

1. Llama-3-8B: 32 layers, 8 KV heads, head dim 128, fp16. KV cache bytes per token?
   Guess:

2. That model on an 80 GB GPU: weights 16 GB, 4 GB overhead, 8,192-token contexts. Max concurrent sequences?
   Guess:

3. New replica of a 70B model: node provisioning 180 s, 12 GB image at 0.2 GB/s, 140 GB weights at 1 GB/s, load to GPU at 2 GB/s. Cold start?
   Guess:

4. $3 per GPU-hour, 2,000 output tokens/s per GPU. Cost per million output tokens? At 20% utilisation?
   Guess:

5. Traffic falls from 100 to 2 requests per second. What does GPU utilisation of each replica show? What does the queue show?
   Guess:

## Misses
-
