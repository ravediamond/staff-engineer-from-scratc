# 16. Streaming and messaging

Week 13. The mechanisms behind "use Kafka", in the order an interviewer digs.

## 1. The log

A topic is split into **partitions**; a partition is an append-only log of records with increasing
**offsets**. Order is guaranteed inside a partition only. On disk: **segments** (1 GB by default), each
with a sparse offset index and a time index; only the last segment is written. Throughput comes from
sequential I/O, the OS page cache, zero-copy sends and end-to-end batching/compression.

Cleanup: `delete` (drop segments older than `retention.ms`, 7 days by default, or beyond
`retention.bytes`) or `compact` (keep the latest record per key; a null value is a tombstone). Tiered
storage (KIP-405, production-ready since 3.9) moves closed segments to object storage.

## 2. Replication and durability

One leader per partition, followers fetch. **ISR** = replicas caught up within
`replica.lag.time.max.ms`. **HW** = min log-end offset over the ISR; consumers read below it.
`acks=0|1|all`; `acks=all` + `min.insync.replicas=2` on RF=3 survives one broker loss without losing
acknowledged writes and refuses writes when two are down. Leader election is from the ISR;
`unclean.leader.election.enable=true` trades committed data for availability. Leader epochs decide
truncation after failover. Metadata (leaders, ISRs, configs) lives in the **KRaft** controller quorum;
Kafka 4.0 (March 2025) removed ZooKeeper.

| Setting | Survives | Costs |
|---|---|---|
| acks=1 | nothing if the leader dies before replication | lowest latency |
| acks=all, min ISR 1 | same as acks=1 when the ISR has shrunk | false confidence |
| acks=all, min ISR 2, RF 3 | one broker | writes blocked with two brokers down |
| min ISR = RF | one broker (data) | every restart blocks writes |

## 3. Producers and consumers

- Partitioner: `hash(key) % partitions`. Adding partitions remaps keys: per-key order breaks across
  the change. Hot keys: salt and re-aggregate, or isolate.
- **Idempotent producer** (PID + per-partition sequence numbers): no duplicates from retries. Default on.
- **Transactions** (`transactional.id`): atomic writes across partitions plus offset commits; readers in
  `read_committed`. Exactly-once for consume-transform-produce **inside Kafka** only.
- **Consumer groups**: one owner per partition; committed offsets in `__consumer_offsets`; rebalances on
  membership change (incremental, broker-driven since KIP-848, GA in 4.0). Commit after processing =
  at-least-once; make the effect idempotent.
- **Lag** = log end − committed. Alert on time lag vs the freshness SLO. Autoscale on lag (KEDA) up to
  the partition count.
- **Share groups** (KIP-932, production-ready in 4.2): queue semantics: many consumers per partition,
  per-record ack/release/reject, redelivery, no ordering.
- Slow handlers: `max.poll.interval.ms` (5 min) kicks the consumer out. Hand off to workers with
  pause/resume, turn the message into a job, or use a share group.

Partition count: `max(target / per-partition throughput, target / per-consumer throughput) × headroom`,
measured, fixed generously at creation.

## 4. Stream processing

Event time vs processing time. **Watermark** = "no more events before W" (per partition:
max event time − bound; job-wide: the minimum). Windows: tumbling, sliding, session. A window fires
when the watermark passes its end; **allowed lateness** keeps state for updates; later events go to a
side output. **Checkpoints** store state together with input offsets (Flink: barrier snapshots);
recovery = restore + replay. Exactly-once output needs a transactional (two-phase commit) or
idempotent sink. Kappa (one streaming path, replay to reprocess) has mostly replaced Lambda (batch +
speed layers); keep batch for reconciliation.

Engines: Kafka Streams (a library, state in RocksDB + changelog topics), Flink (cluster, richest event
time and state), Spark Structured Streaming (micro-batch, fits a Spark shop).

## 5. Getting data in and out without lying

- **Dual write** (DB then broker) loses or invents events. **Outbox**: business row + event row in one
  transaction; a relay publishes. **CDC** (Debezium on Kafka Connect) reads the database log: the
  standard relay. Also the way to build search indexes, caches and feature stores from a database.
- **Schema registry** (Avro/Protobuf/JSON Schema): BACKWARD (new reader, old data; consumers first),
  FORWARD (old reader, new data; producers first), FULL. Add optional fields with defaults; never
  retype, rename or reuse tags. Breaking change = new topic version.
- **Errors**: classify; retry topics with increasing delay; dead-letter queue with original
  coordinates, alert and replay tool. Poison messages vs per-key ordering is a real trade-off.

## 6. Choosing, sizing, operating

| Need | Pick |
|---|---|
| ordered high-throughput log, replay, many consumer groups | Kafka (or Redpanda: same API, simpler ops) |
| task queue, per-message ack, delays, low volume | SQS, RabbitMQ, Postgres `SKIP LOCKED` |
| managed log on one cloud | Pub/Sub (per-message ack, ordering keys), Kinesis (shards) |
| multi-tenancy, storage/compute split | Pulsar |
| lightweight, edge | NATS JetStream |

Numbers to quote and then offer to measure: RF 3 / min ISR 2; 7-day retention; ~1 MB default max
message (bigger payloads: object storage + pointer); 1 GB segments; single-digit ms produce latency in
region when tuned; `linger.ms`/`batch.size` trade latency for throughput; cross-AZ replication traffic
is a first-order cloud cost (the reason for "diskless" designs: KIP-1150 accepted in 2026, not yet
released in Apache Kafka; WarpStream, AutoMQ, Aiven Inkless, Redpanda ship object-storage variants).

Operate on: under-replicated partitions, ISR shrink rate, offline partitions, controller health,
request latency, disk, consumer time lag, DLQ depth. Multi-region: MirrorMaker 2 or cluster linking,
asynchronous, with a stated RPO and an offset-translation runbook.

## The 60-second answer to "design X with Kafka"

Source of truth and outbox/CDC → topic with key = ordering unit, RF 3 / min ISR 2 / acks=all →
schema registry, BACKWARD → consumer groups, commit after processing, idempotent effects → retry
topics and DLQ → stream job with event-time windows if aggregates are needed → lag-based alerts and
autoscaling → say when you would not use Kafka.

## Questions

1. Why can consumers not read above the high watermark?
<details><summary>Answer</summary>Records above it are not yet on every in-sync replica; a failover could erase them after a consumer acted on them.</details>

2. What does `acks=all` guarantee with `min.insync.replicas=1`?
<details><summary>Answer</summary>Only that the current ISR has the record, and the ISR may be the leader alone: leader-only durability in disguise.</details>

3. Where is exactly-once real?
<details><summary>Answer</summary>Inside Kafka with transactions (consume-transform-produce) and inside a stream processor's state with checkpoints. Any external effect needs idempotency or its own transaction.</details>

4. Your consumer group has 12 partitions and 20 pods, and lag grows. What now?
<details><summary>Answer</summary>8 pods are idle. Find the slow handler or hot partition first; then more partitions (new topic if order matters), batching, a worker pool per partition, or a share group if order does not matter.</details>

5. How do you delete one user's data from Kafka?
<details><summary>Answer</summary>Short retention as the SLA, tombstones on compacted topics, or crypto-shredding (delete the per-user key). Plus every downstream copy.</details>
