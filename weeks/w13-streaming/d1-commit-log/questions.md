# Questions

1. Why is an append-only log fast on ordinary disks? Name the three mechanisms Kafka relies on.
2. How does a broker find offset 5,000,000,123 in a partition with 400 segments?
3. Retention vs compaction: what does each guarantee to a consumer that starts from the beginning?
4. What is a tombstone, and why must it be kept for a while before being removed?
5. A user asks for GDPR erasure. Their events are in a 30-day topic and in a compacted topic. What do you do for each?
6. Tiered storage (KIP-405) vs "diskless" topics (KIP-1150): what moves to object storage in each, and which one can you run today on Apache Kafka?

## Model answers

1. Sequential I/O (appends and scans, no seeks); the OS page cache (the broker keeps almost no data on its heap, recent data is served from memory); zero-copy `sendfile` from page cache to socket for plaintext consumers. Plus batching and compression of whole record batches end to end.
2. Segment files are named by base offset: binary search the (in-memory) segment list for the last base ≤ target. Then binary search that segment's sparse, memory-mapped offset index for the last entry ≤ target, seek to its file position, and scan forward a few KB. A separate time index maps timestamps to offsets the same way.
3. Retention: everything from the last `retention.ms` (or bytes), complete history inside that window, nothing before. Compaction: at least the latest value of every key ever written and not deleted (plus a not-yet-compacted tail with full history); enough to rebuild a table, not the history.
4. A record with a null value: "this key is deleted". The compactor removes older values of the key but keeps the tombstone for `delete.retention.ms` (24 h by default) so that consumers that are behind still see the deletion; removed earlier, a slow consumer would keep the old value forever.
5. Time-retained topic: wait out the retention (state it as the deletion SLA; shorten it if 30 days is too long) or use crypto-shredding: per-user key, events encrypted, delete the key. Compacted topic: write a tombstone for the user's key and make sure compaction runs (`min.cleanable.dirty.ratio`, `max.compaction.lag.ms`). Also: downstream copies (warehouse, search index, backups) need their own erasure path; keep PII out of keys and out of long-retention topics by design.
6. Tiered storage keeps the active/recent segments on broker disks and moves closed segments to object storage; brokers still own replication of the hot tail. It is production-ready in Apache Kafka since 3.9. Diskless topics write batches straight to object storage with a small coordinator for ordering, removing broker disks and cross-AZ replication for those topics, at the cost of higher latency. KIP-1150 was accepted in March 2026 but is not in an Apache release yet (as of late 2026); WarpStream, Aiven Inkless, AutoMQ and Redpanda ship object-storage designs. Check the current status before quoting it.
