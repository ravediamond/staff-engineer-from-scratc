# Questions

1. Define recall@k. Why must every ANN benchmark report it alongside latency?
2. IVF vs HNSW: build cost, memory, query speed, update friendliness.
3. 500M vectors × 1024 dims. Raw size? How do you serve it at 2,000 QPS with p99 < 50 ms?
4. Filtered vector search (tenant = X) on a selective filter: what goes wrong with post-filtering, and what are the options?
5. You switch embedding model. What happens to the index, and how do you migrate without downtime?

## Model answers

1. The fraction of the true top-k (exact search) that the ANN index returned, averaged over a query set. An index can be arbitrarily fast at zero recall, so speed claims only mean something at a stated recall on the target data distribution.
2. IVF: cheap build (k-means), compact, easy to add vectors into existing cells (centroids drift and need occasional retraining), recall depends on nprobe. HNSW: slow, memory-heavy build (M links per vector, multiple layers), excellent recall and latency, supports inserts, but deletes are hard (tombstones, rebuilds).
3. 500M × 1024 × 4 B ≈ 2 TB raw. Options: IVF-PQ compression (64–128 B per vector, ~50 GB fits in RAM or GPU) with re-ranking of the top candidates on full-precision vectors from SSD; or shard HNSW across ~20–40 nodes with replicas for QPS. Estimate per-node QPS from benchmarks at the target recall and add headroom. Also consider dimensionality reduction (Matryoshka embeddings truncated to 256 dims).
4. Post-filtering takes the top-k by similarity, then drops non-matching results, so a 1% filter returns about 0.1 results instead of 10, and recall collapses. Options: pre-filter (exact search within the filtered subset when it is small), filter-aware traversal (HNSW with allow-lists, as Qdrant and Weaviate do), per-tenant partitions or indexes for big tenants, or over-fetching k/selectivity with a cap.
5. Vectors from different models live in different spaces, so you cannot mix them: the whole corpus must be re-embedded. Migration: build a new index in parallel (backfill job with checkpoints), dual-write new documents to both, shadow-evaluate retrieval quality on a labelled set and with online A/B, cut over reads with a flag, keep the old index for rollback, then delete it.
