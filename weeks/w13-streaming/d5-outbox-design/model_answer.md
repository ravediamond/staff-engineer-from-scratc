# Model answer: event-driven order platform

**Requirements.** Decouple checkout from five consumers. Ordering unit: the order. Inventory:
effectively-once, in order per order. Notifications: at-least-once, minutes of delay acceptable.
Analytics: per-minute revenue within 30 s, corrected later if needed. Replay: 7 days hot, longer in
object storage. Non-goals for v1: multi-region active-active, exactly-once into third-party systems.

**Numbers.** 20,000 events/s × 1 KB = 20 MB/s in; ×3 replicas = 60 MB/s written. 7 days ≈ 12 TB
before compression ×3 = 36 TB, less with compression and tiered storage. Partitions: if a consumer
instance handles ~2 MB/s, 20 / 2 = 10; ×1.5 headroom, ×2 for growth → 32, fixed at creation. I would
measure both throughputs before committing to the number.

**Diagram.**
```
order-svc -> Postgres (orders + outbox, one transaction) -> Debezium (Kafka Connect)
          -> topic orders.v1 (key = order_id, 32 partitions, RF 3, min ISR 2) + schema registry (BACKWARD)
groups:  inventory     -> idempotent upsert (event_id in the same DB transaction)
         notifications -> retry topics 5s / 1m / 10m -> DLQ (alert, replay tool)
         fraud         -> features -> decisions topic
         search-index  -> OpenSearch (upsert by order_id, version = event sequence)
         analytics     -> Flink: event-time 1-min windows -> ClickHouse (upsert by window + key)
         archive       -> object storage (Parquet) for replay beyond retention and for the warehouse
```

**Path of one event.** Checkout commits the order and its outbox row atomically. Debezium reads the
WAL and produces to `orders.v1` with `acks=all` and idempotence. The partition leader appends; the
record is visible to consumers once it is below the high watermark (on ≥ 2 replicas). Inventory polls,
applies the stock change and inserts the event id in one transaction, then commits the offset.

**Durability and ordering.** RF=3, `min.insync.replicas=2`, `acks=all`, unclean election off: one
broker can fail with no loss of acknowledged data and no write outage; a second failure stops writes
rather than risk loss. Order is per partition, so per order id. Adding partitions later would remap
keys; I over-provision and, if ever needed, migrate to a new topic at a clean cut.

**Delivery semantics.** Everything is at-least-once by construction (CDC restarts, consumer crashes).
Inventory and search are idempotent by event id / version. Kafka transactions give exactly-once only
for Kafka-to-Kafka steps (the Flink job uses checkpoints and an idempotent ClickHouse upsert instead).
Notifications deduplicate on event id with a TTL store; a rare duplicate email is acceptable and stated.

**Failures.** Broker loss: leader moves to an ISR member, clients retry. Consumer crash: rebalance,
resume from the committed offset. Poison message: non-retryable → DLQ at once with the original
coordinates; retryable → delayed retry topics, then DLQ; for inventory, later events of the same order
follow the blocked one. Downstream down for 2 h: pause, lag grows, well inside retention; alert on time
lag vs each consumer's SLO. Region loss: v1 is single region, three AZs; MirrorMaker 2 to a second
region as phase 2 with an explicit RPO of seconds and a tested offset-translation runbook.

**Analytics.** Event time from the order, 1-minute tumbling windows, watermark bound 5 s, early
firing every 10 s, allowed lateness 10 min with updates, later events to a side topic. Nightly batch
recomputation from the archive reconciles revenue.

**Contracts and evolution.** Avro or Protobuf in a registry, BACKWARD mode, consumers deploy first.
Additive changes only; a rename is a new topic version with dual publishing and a retirement date.
PII stays out of keys; erasure by tombstone or crypto-shredding plus the archive's own process.

**Operations.** Dashboards and alerts: time lag per group, under-replicated partitions, ISR shrink
rate, produce error rate, DLQ depth and age, Connect task state, end-to-end latency from outbox insert
to consumer effect. Capacity alarm on disk and on partition leader skew.

**Judgment.** At 50 events/s with one consumer I would not run Kafka: an outbox table polled with
`SKIP LOCKED`, or SQS/Pub/Sub. Kafka earns its cost here through six independent consumers, replay
and ordered high throughput. Managed Kafka (MSK, Confluent, Aiven) unless there is a platform team.
