# Rubric

Score each line 0 / 1 / 2.

| # | Criterion | Senior signal (1) | Staff signal (2) |
|---|---|---|---|
| 1 | Requirements | lists consumers | ordering unit, latency per consumer, retention/replay need, delivery requirement per consumer, non-goals |
| 2 | Estimation | events/s | MB/s in and replicated, storage for the retention, partitions derived from measured per-partition and per-consumer throughput, cross-AZ cost noted |
| 3 | Producing | "service publishes to Kafka" | names the dual-write problem; outbox + CDC (or equivalent); key = order id; idempotent producer |
| 4 | Durability | "replicated" | RF=3, min ISR 2, acks=all, unclean election off, and the failure each setting covers |
| 5 | Ordering & scaling | "partition by key" | per-key order only; partition count over-provisioned; cost of adding partitions; hot keys; parallelism cap; share groups or worker hand-off for slow work |
| 6 | Consumer semantics | "at-least-once" | commit after processing; idempotent effect with the event id in the same transaction; where Kafka transactions apply and where they do not |
| 7 | Stream processing | "a Flink job" | event time, watermark bound, allowed lateness, late side output, checkpointed state, idempotent OLAP sink |
| 8 | Failure handling | DLQ mentioned | error classes, retry topics with delay, DLQ with replay tool and alert, downstream outage absorbed by lag within retention, poison message vs ordering |
| 9 | Contracts | "schema registry" | compatibility mode, deploy order, breaking change via versioned topic, ownership of the contract, PII and erasure |
| 10 | Operations & judgment | "monitoring" | lag in seconds vs SLO, ISR shrink, under-replicated partitions, DLQ depth; multi-region stance with RPO; when NOT to use Kafka; v1 scope |

0–9 senior or below · 10–14 senior+ · 15–17 staff · 18–20 strong staff.
