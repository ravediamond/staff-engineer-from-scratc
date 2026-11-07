# Questions

1. Explain ring all-reduce in two phases. Why is it bandwidth-optimal?
2. Ring vs tree all-reduce: when does each win?
3. Estimate gradient all-reduce time for a 7B model on 64 GPUs across 8 nodes with 400 Gb/s per node.
4. How does DDP overlap communication with computation?
5. What is the difference between all-reduce, reduce-scatter and all-gather, and where does FSDP use each?

## Model answers

1. Reduce-scatter: N−1 steps where each worker passes one chunk around the ring and accumulates, ending with each worker owning one fully reduced chunk. All-gather: N−1 steps circulating the completed chunks. Each worker sends and receives 2(N−1)/N of the buffer, which matches the lower bound for all-reduce, and all links are used simultaneously.
2. Ring: bandwidth-optimal, latency grows linearly with N (2(N−1) steps), so it is good for large messages. Tree (or recursive halving/doubling): log N latency steps, better for small messages and very large N. NCCL picks by message size and topology, and uses hierarchical schemes (within node over NVLink, across nodes over IB).
3. 7B × 2 bytes = 14 GB of bf16 gradients. The inter-node ring is the bottleneck: each node sends about 2 × 14 GB × 7/8 ≈ 24.5 GB through 50 GB/s (400 Gb/s) ≈ 0.5 s per step if not overlapped. With hierarchical all-reduce (reduce in-node first) the inter-node volume per node stays similar but there are fewer participants; overlapping with backward hides most of it if compute per step exceeds ~0.5 s.
4. Gradients are grouped into buckets (~25 MB) in reverse layer order; when all gradients in a bucket are ready during backward, its all-reduce is launched asynchronously, so communication of late layers overlaps computation of earlier layers. The optimizer step waits for all buckets.
5. All-reduce: everyone gets the full reduced tensor. Reduce-scatter: everyone gets one reduced shard. All-gather: everyone gets the concatenation of all shards. FSDP all-gathers parameters before each layer's forward and backward, and reduce-scatters gradients after backward so each rank keeps only its shard (all-reduce = reduce-scatter + all-gather, split across the step).
