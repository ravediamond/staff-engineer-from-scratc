# Questions (answer with numbers, out loud, under 60 s each)

1. Estimate the QPS and storage for a URL shortener with 100M new URLs/month and 10:1 read/write.
2. Estimate how many GPUs to serve a 70B model chat product at 200 req/s peak, 1,500 in / 300 out tokens. State the per-GPU numbers you assume.
3. Estimate embedding 50M documents of 2,000 tokens with a model that does 30,000 tokens/s per GPU. GPU-hours and dollars at $2/h.
4. Your estimate says 4 GPUs; production needs 11. List the four most likely reasons.
5. Why do staff engineers estimate cost and not just capacity?

## Model answers

1. Writes: 100M / (30 × 86,400) ≈ 40/s; reads ≈ 400/s average, ~2k/s peak. Storage: ~500 B per URL × 100M × 12 ≈ 600 GB/yr, about 3 TB over 5 years with indexes; trivially one primary + replicas. The hard parts are ID generation and caching, not scale.
2. Assume tensor-parallel replicas of 4 GPUs (70B in fp8 or bf16), each replica doing ~2,500 decode tok/s aggregate and ~25k prefill tok/s. Per second: 200 × 300 = 60k decode tokens → 24 replicas; 200 × 1,500 = 300k prefill tokens → 12 replicas-worth. Decode and prefill share GPUs, so about 36 replicas ≈ 144 GPUs, plus ~30% headroom ≈ 190 GPUs. Then: is that $300k+/month justified, or can a smaller distilled model handle 70% of traffic?
3. 50M × 2,000 = 10^11 tokens / 30k tok/s = 3.3M GPU-seconds ≈ 926 GPU-hours ≈ $1,850. Parallel on 50 GPUs: under a day. Add 20% for retries and overhead.
4. Batching efficiency far below benchmark (real request mix, long contexts, KV-cache memory limits); peak-to-average ratio higher than assumed; output lengths longer than estimated (long tail); headroom for failures and deploys (N+1, rolling restarts); and per-replica minimums such as tensor parallelism or one replica per region.
5. Because cost picks the design: the dominant cost term is where optimization, caching, model choice and the build-vs-buy decision matter. It also shows business judgment, which is part of the staff bar ("this feature costs $0.04 per user per day; is it worth it?").
