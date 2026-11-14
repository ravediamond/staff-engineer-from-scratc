# Questions

1. How does MVCC let readers and writers not block each other? What is a snapshot made of in Postgres?
2. Name the anomaly each level still allows: read committed, repeatable read/snapshot, serializable.
3. Three ways to fix a lost update in application code, and when you would choose each.
4. Write skew: give an example from your own domain and two fixes.
5. What does VACUUM do, and what are the two classic production problems around it?
6. `SELECT … FOR UPDATE`, `FOR UPDATE SKIP LOCKED`, optimistic locking with a version column: what is each for?

## Model answers

1. Writers create new row versions instead of overwriting; each version records the creating (xmin) and deleting (xmax) transaction. A reader evaluates each version against its snapshot and ignores what it should not see, so it never waits for a writer and a writer never waits for a reader. A Postgres snapshot is (xmin: oldest transaction still running, xmax: first id not yet assigned, the list of in-progress ids between them) plus the commit log to know whether an id committed or aborted.
2. Read committed: non-repeatable reads, phantoms, lost updates from read-modify-write, write skew. Repeatable read (snapshot isolation in Postgres): write skew and other read-only-dependent anomalies; lost updates are detected (serialization failure). Serializable (SSI in Postgres): none; transactions may be aborted and must be retried.
3. (a) Atomic statement: `UPDATE t SET n = n + 1 WHERE id = …`: simplest, when the change is expressible in SQL. (b) Pessimistic: `SELECT … FOR UPDATE` then update: when logic must run between read and write and contention is high. (c) Optimistic: version column, `UPDATE … WHERE id = … AND version = :v`, retry on zero rows: when conflicts are rare or the read and write are in different requests. Or raise the isolation level and retry on serialization failures.
4. Example: "a GPU quota of 8 per team": two concurrent job submissions each check `SUM(gpus) ≤ 8 − request`, both pass, both insert: over quota. Each wrote a different row, so snapshot isolation sees no conflict. Fixes: serializable isolation with retries; or materialise the conflict: lock a parent row (`SELECT … FOR UPDATE` on the team row) or keep a counter row that both must update; or a database constraint (exclusion constraint, unique index) when the invariant can be expressed as one.
5. It removes row versions no snapshot can see, makes the space reusable, updates visibility maps and statistics, and freezes old transaction ids. Problems: (1) long-running transactions or stale replication slots hold the horizon back, dead tuples accumulate, tables and indexes bloat and queries slow down; (2) transaction-id wraparound: if autovacuum cannot freeze old rows in time, Postgres forces aggressive vacuums and ultimately stops accepting writes.
6. `FOR UPDATE`: lock the selected rows until the end of the transaction so that a read-modify-write is safe; others wait. `FOR UPDATE SKIP LOCKED`: take rows nobody else has locked and skip the rest: a job queue on a table, many workers, no double processing. Optimistic locking: no lock held between read and write (works across HTTP requests); the write succeeds only if the version is unchanged, otherwise the client reloads and retries.
