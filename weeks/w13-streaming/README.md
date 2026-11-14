# Week 13: streaming and messaging (Kafka from the inside)

"Design a basic architecture with a streaming technology like Kafka" is a standard staff prompt, and
"design Kafka itself" is a reported Meta E6 prompt. You cannot answer either from a diagram of boxes:
the follow-ups go one level down (ISR, high watermark, rebalances, watermarks, outbox). This week you
build each mechanism small enough to read in one sitting, then design with them on Friday.

Primer: `knowledge/16-streaming-and-messaging.md`. Hands-on with a real broker: `handson/kafka/README.md`
(do it after d3: simulate the invariant first, then break the real thing the same way).

| Day | Lab | Review bug |
|---|---|---|
| d1 | commit log: segments, sparse index, retention, compaction | compaction renumbers offsets |
| d2 | replication: ISR, high watermark, acks, leader failover | high watermark taken from the leader's end offset |
| d3 | clients: partitioner, idempotent producer, consumer groups, lag | zombie consumer commits after a rebalance |
| d4 | stream processing: event time, watermarks, lateness, checkpoints | watermark = max across partitions |
| d5 | outbox + CDC relay, idempotent consumer, schema compatibility + **design #7** | marked as published before publishing |
