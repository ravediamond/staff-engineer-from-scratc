# W13 D3: producers and consumer groups

Primer: `knowledge/16-streaming-and-messaging.md` §3.

## The one idea

**Producer side.** The partition is `hash(key) % n_partitions`: same key → same partition → ordered.
Change `n_partitions` and most keys move: per-key order breaks across the change. A network timeout
makes the producer retry, and the broker may already have the record: duplicates. The **idempotent
producer** fixes it: each producer has an id (PID) and numbers its records per partition; the broker
accepts `seq = last + 1`, drops `seq ≤ last` as a duplicate (and still acknowledges), and rejects gaps.

**Consumer side.** Consumers with the same `group.id` share the partitions: each partition is owned by
**one** member of the group. Membership changes trigger a **rebalance**, which bumps the group
**generation**. The group stores a **committed offset** per partition. **Lag** = log end − committed.

The classic failure: a consumer stalls (long GC, 10-minute handler > `max.poll.interval.ms`), is
kicked out, its partitions go to someone else, then it wakes up and commits its old position. The
coordinator must reject commits from an old generation: the same **fencing** idea as your W3 leases.

Parallelism of a group is capped by the partition count. For work-queue workloads (no ordering, slow
handlers) **share groups** ("queues for Kafka", KIP-932, production-ready in Kafka 4.2) let many
consumers read one partition with per-record acknowledgement.

## Today's build (`w13d3_clients.py`)

`partition_for`, `moved_fraction`, `IdempotentBroker`, `range_assign`, `GroupCoordinator`.

## Staff angle

Three numbers decide a topic: partitions (parallelism and ordering unit), key (what must stay in
order), and consumer lag (the health metric you alert on, in seconds behind rather than messages).
