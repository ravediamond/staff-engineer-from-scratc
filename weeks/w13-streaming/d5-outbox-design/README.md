# W13 D5: outbox, CDC, schema compatibility + design #7

Primer: `knowledge/16-streaming-and-messaging.md` §5–6.

## The one idea

A service that changes its database **and** publishes an event has a **dual-write** problem: there is no
transaction across Postgres and Kafka. Crash between the two and either the order exists with no event
(lost) or the event exists with no order (phantom).

**Transactional outbox:** in the SAME database transaction, write the business row and an `outbox` row
describing the event. A separate **relay** reads the outbox in order and publishes. In production the
relay is **CDC**: Debezium tails the database's write-ahead log and turns committed outbox inserts into
Kafka records. The relay is **at-least-once** (publish, then mark; a crash in between republishes), so
every consumer must be **idempotent**: store the event id in the same transaction as the effect (W4 D5).

**Schemas** are the contract between teams that deploy at different times. With a schema registry:

| Mode | Rule | Who upgrades first |
|---|---|---|
| BACKWARD | the new schema can read data written with the old one | consumers |
| FORWARD | the old schema can read data written with the new one | producers |
| FULL | both | any order |

In practice: you may add a field **with a default**, or remove one that had a default. Never change a
type, rename, or reuse a field number/tag.

## Today's build (`w13d5_outbox.py`)

`place_order` (one transaction), `relay_once`, `InventoryConsumer.handle`, `backward_compatible`,
`forward_compatible`, `partitions_needed`. SQLite in memory stands in for Postgres.

Then **design #7** (`design.md`, 45 minutes, graded with `rubric.md`).

## Staff angle

Saying "we publish an event after the commit" in a design review is the tell of someone who has not
run this in production. Say "outbox + CDC, at-least-once, idempotent consumers keyed by event id",
then say what you would do if the team is too small to run Kafka at all (Postgres `SKIP LOCKED`, SQS).
