# Week 15: databases

"Which isolation level, and why?" "Why is this query slow?" "How do you not double-charge?" Staff
design rounds end up in the database, and Part 1 only covered the storage engine side (WAL, LSM).
This week: concurrency control, indexes, SQL you can write under pressure, replication as seen by the
application, and money.

Primer: `knowledge/19-databases.md`.

| Day | Lab | Review bug |
|---|---|---|
| d1 | MVCC: snapshots, read committed vs snapshot vs serializable, lost update, write skew, vacuum | commits made after the snapshot are visible |
| d2 | B+tree: search, insert with splits, range scans; which index serves which query | range scan stops at the end of the leaf |
| d3 | SQL under pressure (SQLite): top-N per group, running totals, anti-joins, sessions, EXPLAIN | `NOT IN` with a NULL |
| d4 | replication from the application's side: lag, read-your-writes, failover and what is lost | reads routed by replica health only |
| d5 | money: double-entry ledger, idempotent transfers, seat holds, reconciliation | amounts stored as floats |
