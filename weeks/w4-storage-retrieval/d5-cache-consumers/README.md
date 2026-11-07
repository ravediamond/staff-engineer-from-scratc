# W4 D5: cache-aside with single-flight, exactly-once consumer

Primer: `knowledge/04-storage-and-retrieval.md` §5.

## The one idea

**Cache-aside:** read cache; on miss, load from the source of truth, fill the cache. Two production
failure modes:

1. **Stampede (dogpile):** a hot key expires, 5,000 concurrent requests miss at once, 5,000 loads hit
   the database. Fix: **single-flight**: the first miss loads, the others await the same future.
   (Also: jittered TTLs, early probabilistic refresh.)
2. **Stale after write:** the standard order is "write DB, then **delete** the cache key" (not set it:
   two concurrent writers setting values can leave the older one in the cache).

**Exactly-once consumer.** A consumer reads messages from a log at offsets. The two orders:

| Order | Crash between the two steps | Result |
|---|---|---|
| commit offset, then process | message never processed | **lost** (at-most-once) |
| process, then commit offset | message processed again on restart | **duplicate** (at-least-once) |

Exactly-once **effect** = process-then-commit **plus** idempotent processing: store the processed
message id **atomically with the effect**, and skip ids already applied.

## Today's build (`w4d5_cache_consumer.py`)

- `SingleFlightCache(loader, ttl, clock)`: async `get(key)`; concurrent misses for a key share one `loader` call; `loads` counter.
- `Sink`: holds `total` and `applied_ids`; `apply(msg_id, amount)` adds atomically, skipping seen ids.
- `Consumer(log, sink)`: `run(crash_after_effect_at=None)` processes from the committed offset;
  simulates a crash right after the effect of a given offset, before commit. Re-running resumes.

## Staff angle

In ML systems the "consumer" is everywhere: the embedding pipeline reading a CDC stream, the
eval harness consuming a queue of model checkpoints, the feature pipeline writing to an online
store. A staff design review asks of each one: what is the delivery semantics, where is the
offset stored, what makes the write idempotent, and what does a replay from offset 0 cost?
