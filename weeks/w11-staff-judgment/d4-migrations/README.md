# W11 D4: live migrations

Primer: `knowledge/12-staff-rubrics.md` §5.

## The one idea

Moving a live system (new vector DB, new schema, new embedding model, new feature store) without
downtime is a staff rite of passage. The pattern is always the same:

```
dual_write ─▶ backfill ─▶ verify ─▶ cutover_reads ─▶ stop_old_writes ─▶ cleanup
    (rollback possible at every phase up to and including cutover_reads; after stop_old_writes, the old store is stale)
```

- **Dual write**: every write goes to old and new. New data is covered from now on.
- **Backfill**: copy history, in key order, in batches, **resumable** from a checkpoint, **idempotent**
  (a key copied twice is fine; a newer dual-written value must not be overwritten by stale backfill data:
  compare versions).
- **Verify**: compare old vs new on all keys or a large sample; the mismatch rate must be under a threshold.
- **Cutover**: only after verification passes. Reads flip (behind a flag), old writes continue so rollback is instant.
- Only then stop old writes and clean up.

**Invariant:** at every moment, one store is fully correct and reads come from it.

## Today's build (`w11d4_migration.py`)

`backfill(old, new, batch, checkpoint)` → new checkpoint (versions respected), `verify(old, new)` → `(mismatch_rate, keys)`,
`Migration(threshold)` state machine with `advance(**evidence)`, `rollback()`, and `read_from()`.

## Staff angle

The technical steps are known; the staff work is the plan: which teams are affected, the comms, the
success metrics per phase, the rollback trigger written down **before** starting, and who can press it.
Migrations fail on the 5% of weird data (orphans, encodings, nulls) and on the 1% of clients nobody
knew about: budget time for both.
