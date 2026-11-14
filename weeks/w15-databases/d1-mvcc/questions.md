# Questions

1. How does MVCC let readers and writers not block each other? What is a snapshot made of in Postgres?
2. Name the anomaly each level still allows: read committed, repeatable read/snapshot, serializable.
3. Three ways to fix a lost update in application code, and when you would choose each.
4. Write skew: give an example from your own domain and two fixes.
5. What does VACUUM do, and what are the two classic production problems around it?
6. `SELECT … FOR UPDATE`, `FOR UPDATE SKIP LOCKED`, optimistic locking with a version column: what is each for?

