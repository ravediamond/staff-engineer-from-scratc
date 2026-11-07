# Week 4: storage, search and retrieval infrastructure

RAG is a storage system with a language model bolted on top. Before you can design one at staff
level, you need to know what is under a vector database and a search engine: logs, sorted runs,
probabilistic filters, inverted indexes, approximate nearest neighbours, caches, and consumers
that do not lose or duplicate work. This week builds all of them small enough to read in one
sitting.

Primer: `knowledge/04-storage-and-retrieval.md`.

| Day | Lab | Review bug |
|---|---|---|
| d1 | write-ahead log + LSM tree (memtable, SSTables, recovery) | reads SSTables oldest first |
| d2 | bloom filter + compaction | compaction keeps the oldest version |
| d3 | inverted index + BM25 + boolean AND | length normalisation inverted |
| d4 | vector search: brute force, IVF, greedy graph search, recall@k | cosine without normalisation |
| d5 | cache-aside with single-flight, exactly-once consumer | offset committed before processing |
