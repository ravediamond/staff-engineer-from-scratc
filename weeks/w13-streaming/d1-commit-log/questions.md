# Questions

1. Why is an append-only log fast on ordinary disks? Name the three mechanisms Kafka relies on.
2. How does a broker find offset 5,000,000,123 in a partition with 400 segments?
3. Retention vs compaction: what does each guarantee to a consumer that starts from the beginning?
4. What is a tombstone, and why must it be kept for a while before being removed?
5. A user asks for GDPR erasure. Their events are in a 30-day topic and in a compacted topic. What do you do for each?
6. Tiered storage (KIP-405) vs "diskless" topics (KIP-1150): what moves to object storage in each, and which one can you run today on Apache Kafka?

