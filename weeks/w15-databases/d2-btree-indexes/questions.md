# Questions

1. B-tree vs LSM-tree: write path, read path, space, and which workloads favour each.
2. Why does a B+tree keep values only in leaves and link the leaves?
3. Composite index column order: state the rule and apply it to `WHERE tenant_id = ? AND created_at > ? ORDER BY created_at DESC LIMIT 20`.
4. What is a covering index, and what does it cost?
5. A query is slow. Walk through how you read `EXPLAIN (ANALYZE, BUFFERS)` and the five most common causes.
6. When do indexes hurt? Give four cases.

## Model answers

1. B-tree: update pages in place (plus WAL), one random write per touched page; reads are one root-to-leaf walk, predictable; some space lost to half-full pages and bloat. LSM: append to a memtable and WAL, flush sorted runs, compact in the background: sequential writes, high ingest, good compression; reads may check several runs (Bloom filters help), compaction causes write amplification and latency spikes, deletes are tombstones. B-tree: read-heavy OLTP, range scans, strong latency SLOs (Postgres, MySQL/InnoDB). LSM: write-heavy and time-series workloads, SSD-friendly large datasets (RocksDB, Cassandra, ScyllaDB, most distributed SQL storage layers).
2. Keeping only keys in internal nodes maximises fan-out, so the tree is shallower and the upper levels fit in memory. Linked leaves make range scans and ordered traversals a sequential walk without going back up the tree.
3. Equality columns first, then the range or sort column; then columns only filtered or returned. Here: `(tenant_id, created_at)`: seek to the tenant's newest entry and read 20 index entries backwards: no sort, no scan of the tenant's whole history. With `(created_at, tenant_id)` the database would scan all tenants' recent rows.
4. An index that contains every column the query needs (key columns or `INCLUDE` columns), allowing an index-only scan with no heap access. Cost: a bigger index (more memory and I/O), more work on every write, fewer HOT updates in Postgres when included columns change; and in Postgres an index-only scan still needs the visibility map to be current (vacuum).
5. Find the node with the largest actual time; compare estimated and actual rows (large gaps mean stale statistics or correlated predicates → `ANALYZE`, extended statistics); look at buffers (many reads = cold cache or too much data touched). Common causes: missing or unusable index (function on the column, wrong column order, implicit cast); a sequential scan chosen because of bad row estimates; a nested loop over many rows because of a misestimate; sorts or hash tables spilling to disk (`work_mem`); fetching far more rows than needed (no LIMIT pushdown, N+1 queries from the ORM); lock waits rather than execution time.
6. Write-heavy tables (every index is another structure to update and to log); low-selectivity columns (the planner prefers a scan anyway); many overlapping indexes (memory pressure, slower vacuum); random-key indexes (UUIDv4) larger than memory: each insert is a cache miss; unused indexes kept "just in case". Also index builds and changes on large tables need care (`CREATE INDEX CONCURRENTLY`).
