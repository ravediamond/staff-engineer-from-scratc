# W13 D1: the commit log

Primer: `knowledge/16-streaming-and-messaging.md` §1.

## The one idea

A Kafka partition is an **append-only log**. Every record gets the next **offset**; offsets are never
reused and never change. Everything else in Kafka (replication, consumer groups, exactly-once) is
bookkeeping about offsets in this log.

On disk the log is cut into **segments** (default 1 GB). Only the last one, the **active segment**, is
written. Each segment has a **sparse index**: one entry (offset → position) every few KB. A read does:
binary search the segments by base offset → binary search the sparse index → short linear scan.

Two cleanup policies, both working on **closed** segments only:

- **Retention (`delete`)**: drop whole segments whose newest record is older than `retention.ms`
  (default 7 days). The log start offset moves forward; a consumer asking for a deleted offset gets
  `OffsetOutOfRange` and falls back to `auto.offset.reset`.
- **Compaction (`compact`)**: keep only the **latest record per key**. A record with value `None` is a
  **tombstone**: it deletes the key. Offsets of surviving records do not change, so the log gets gaps.
  This turns a topic into a replayable table (the `__consumer_offsets` topic works this way).

## Today's build (`w13d1_log.py`)

`PartitionLog(segment_records, index_every)`: `append`, `read(offset, max_records)`,
`apply_retention(now, retention_ms)`, `compact()`.

## Staff angle

Sequential appends plus the page cache are why one broker moves hundreds of MB/s on ordinary disks,
and why "Kafka as a queue with random deletes" is the wrong mental model. When you propose a topic in
a design, say its cleanup policy and retention out loud: they decide whether a new consumer can
rebuild its state by replay (the Kappa argument) and what a GDPR deletion costs.
