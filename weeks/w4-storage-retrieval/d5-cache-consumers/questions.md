# Questions

1. Cache stampede: what is it and three mitigations?
2. On write, why delete the cache key instead of setting it?
3. At-most-once, at-least-once, exactly-once: define each in terms of offset commit order.
4. Where must the processed-message id be stored for exactly-once effects, and why there?
5. Your embedding pipeline consumes a CDC stream of document updates. Describe its delivery semantics end to end, and what happens on replay.

## Model answers

1. Many concurrent misses on the same key (usually right after expiry) all hit the backend at once. Mitigations: single-flight/request coalescing, TTL jitter, early probabilistic refresh (refresh before expiry with rising probability, XFetch), serving stale while revalidating, and locks or leases per key (memcached leases).
2. Two writers can interleave: A writes the DB, B writes the DB, B sets the cache, A sets the cache, and the cache holds A's older value indefinitely. Deleting makes the next reader load the current DB value. A narrow race remains with a concurrent reader (read old, write new, delete, set old); leases or versioned values close it.
3. At-most-once: commit then process (crash loses the message). At-least-once: process then commit (crash duplicates it). Exactly-once effect: at-least-once plus idempotent or transactional processing, where the effect and the dedup record (or the offset) commit atomically.
4. In the same transaction as the effect, in the same store. Otherwise a crash between "effect" and "record id" re-applies on replay, and a crash between "record id" and "effect" loses it. If the sink is external and non-transactional, use the sink's own idempotency key.
5. At-least-once from the CDC log (Debezium/Kafka). The embedder processes, then commits offsets. Writes to the vector store are upserts keyed by (doc_id, chunk_id, embedding_model_version), with the source version or LSN stored, and an update is ignored if an equal or newer version is already there (handles reordering). Deletes propagate as tombstones. Replay from offset 0 re-embeds everything (costly but correct): budget it, rate-limit it, and use it as the re-embedding path for model migrations.
