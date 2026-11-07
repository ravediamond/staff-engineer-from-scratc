# Questions

1. Define recall@k. Why must every ANN benchmark report it alongside latency?
2. IVF vs HNSW: build cost, memory, query speed, update friendliness.
3. 500M vectors × 1024 dims. Raw size? How do you serve it at 2,000 QPS with p99 < 50 ms?
4. Filtered vector search (tenant = X) on a selective filter: what goes wrong with post-filtering, and what are the options?
5. You switch embedding model. What happens to the index, and how do you migrate without downtime?

