# Questions

1. Why is a lease-based lock unsafe on its own? Give the timeline.
2. How do fencing tokens fix it, and what must the storage support?
3. Your storage is S3 (no compare on a custom token). How do you fence checkpoint writes from two trainers?
4. Agents pull tasks from a queue with a 5-minute visibility timeout. A task takes 7 minutes. What happens and how do you fix it?
5. When is "just use a lock" the wrong design entirely?

## Model answers

1. A acquires a 10 s lease, then pauses 15 s (GC, VM stall, network). The lease expires, B acquires and writes. A wakes, still believes it holds the lock, and writes. Both act as holder. The client cannot detect this from its own clock without a bound on pauses, and there is none.
2. Each grant carries a strictly increasing token. The resource stores the highest token seen and rejects lower ones, so A's late write with 33 fails after B wrote with 34. The storage needs an atomic check-and-set on (token, write): a conditional write, a transaction, or a single-threaded owner.
3. Put the run generation in the path (`ckpt/gen-34/step-1000`) and have a manifest updated with a conditional write (S3 conditional PUT with `If-Match` on the ETag, or a metadata store like DynamoDB/etcd with compare-and-swap) that refuses generations below the current one. Readers trust only the manifest. An old trainer can write orphan files but can never become "the checkpoint".
4. The message becomes visible again at 5 min, a second agent picks it up, and both execute (duplicate side effects). Fixes: heartbeat to extend visibility while working, make side effects idempotent with a key per task, and fence completion (the ack carries the receipt handle or attempt number; a stale attempt's result is dropped).
5. When the work can be partitioned so each item has one owner (shard by key, single writer per partition), when operations can be made commutative or idempotent (CRDTs, upserts), or when a database transaction or unique constraint gives the guarantee directly. Distributed locks add a failure mode; prefer designs that do not need mutual exclusion.
