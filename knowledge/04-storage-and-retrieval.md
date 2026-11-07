# 04. Storage and retrieval

## §1 Logs and LSM trees

WAL first, then memtable; flush to immutable sorted SSTables; reads go newest to oldest; deletes are
tombstones. Write amplification from compaction, read amplification from multiple runs. B-trees:
in-place updates, better reads, worse random writes.

## §2 Bloom filters and compaction

9.6 bits per key for 1% false positives, k = (m/n) ln 2. No false negatives. Compaction = k-way merge
keeping the newest version; drop tombstones at the bottom level. Leveled (read-optimised) vs size-tiered
(write-optimised).

## §3 Inverted indexes and BM25

Postings per term; BM25 with k1 (tf saturation) and b (length normalisation); boolean AND from the
shortest postings list. Analyzers matter more than parameters (tokenization, stemming, accents).
Document-partitioned sharding with fan-out and merge.

## §4 Approximate nearest neighbour

Flat (exact), IVF (cells, nprobe), HNSW (graph, ef), PQ compression (bytes per vector). Recall@k at a
latency on your data is the only honest benchmark. Filtered search is the production pain point.
Memory: N × d × 4 bytes raw; HNSW adds M links per vector.

## §5 Caches and consumers

Cache-aside with single-flight and jittered TTLs; delete on write; leases for the read/write race.
Consumers: commit after processing; idempotent effects keyed by message id stored atomically with the effect.

## Numbers to know

| Thing | Order of magnitude |
|---|---|
| RAM random read | ~100 ns |
| NVMe SSD random read | ~20–100 µs |
| Same-datacenter round trip | ~0.5 ms |
| Paris ↔ US East round trip | ~80 ms |
| Sequential read, NVMe | 2–7 GB/s |
| 1M × 1024-dim float32 vectors | 4 GB |

## Questions

1. You need full-text search plus vector search plus filters on 50M documents. One system or two?
<details><summary>Answer</summary>Start with one that does all three well enough (OpenSearch/Elasticsearch with kNN, Vespa, Qdrant/Weaviate with sparse vectors) for operational simplicity, and measure. Split into two specialized systems with app-level fusion only if quality, latency or cost demands it, accepting the consistency and operational cost.</details>

2. Why might Postgres + pgvector be the right answer, and when does it stop being right?
<details><summary>Answer</summary>Right when data is already in Postgres, vectors number in the low millions, you need transactions with ACLs and metadata, and the team knows Postgres: one system, joins, consistency. It stops being right at hundreds of millions of vectors, high QPS with strict p99, or when index build and update costs interfere with the OLTP workload.</details>

3. A cache in front of an LLM: exact-match vs semantic cache. Risks?
<details><summary>Answer</summary>Exact match is safe but has low hit rates. A semantic cache (embedding similarity) gets higher hits but can return an answer to a subtly different question (wrong numbers, wrong entity), and leaks across permission boundaries if not keyed by ACL group. Use high similarity thresholds, per-tenant keys, TTLs, and evaluate the false-hit rate on labelled near-duplicates.</details>
