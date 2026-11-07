# W4 D4: vector search: brute force, IVF, graphs, recall@k

Primer: `knowledge/04-storage-and-retrieval.md` §4. Used in W6 D2.

## The one idea

Exact k-NN over N vectors of dimension d costs O(N·d) per query. At 100M × 1024 floats that is
400 GB scanned per query: no. **Approximate** nearest neighbour (ANN) indexes trade recall for speed.

| Index | Build | Query | Knob | Used in |
|---|---|---|---|---|
| Flat (brute force) | none | O(N·d) | — | ground truth, small N, GPU |
| **IVF** | k-means into `nlist` cells | scan `nprobe` nearest cells | nprobe ↑ = recall ↑, latency ↑ | FAISS, Milvus, pgvector ivfflat |
| **Graph (HNSW)** | link each vector to M neighbours | greedy best-first walk | `ef` ↑ = recall ↑ | FAISS, Qdrant, Weaviate, pgvector hnsw |
| + PQ | compress vectors to bytes | approximate distances | code size | billion-scale |

**Recall@k** = |approx top-k ∩ exact top-k| / k, averaged over queries. Every ANN claim must come
with a recall number at a latency, measured on **your** data.

**Cosine similarity** = dot product of **L2-normalised** vectors. Skip normalisation and long
vectors win regardless of direction.

Today's graph index is a simplified NSW: an exact k-NN graph (fine at lab scale) **plus a few random
long-range links**, searched with the same greedy best-first beam (`ef`) HNSW uses on each layer.
Try `n_random=0` after the tests pass: on clustered data recall collapses to near zero, because the
graph splits into islands. HNSW solves the same problem with its sparse upper layers.

## Today's build (`w4d4_vectors.py`, numpy)

`normalize`, `exact_topk(X, q, k)` (cosine), `kmeans(X, k, iters, seed)`, `IVFIndex(nlist).fit(X)` /
`search(q, k, nprobe)`, `KNNGraphIndex(M, n_random).fit(X)` / `search(q, k, ef, entry=0)`, `recall_at_k`.

## Staff angle

The staff question is never "HNSW or IVF?" in the abstract. It is: N, d, QPS, p99 target, update
rate, memory budget, filtering needs. HNSW is fast with high recall but memory hungry (vectors +
M links each) and slow to build. IVF-PQ fits a billion vectors on one GPU box at lower recall.
Filtered search (ACL, tenant, date) is where most production pain is: post-filtering destroys
recall for selective filters (W6 D5).
