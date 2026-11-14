# 19. Databases

Week 15. The storage-engine side (WAL, LSM, Bloom filters) is in `04`. This is what design and
"why is it slow / why is it wrong" rounds ask.

## 1. Transactions and isolation

ACID: atomic (all or nothing: WAL), consistent (your invariants: constraints), isolated (this
section), durable (fsync, replication). **MVCC**: writers add row versions; readers use a snapshot;
neither blocks the other. Postgres row versions carry `xmin`/`xmax`; VACUUM removes dead ones.

| Level (Postgres) | Snapshot | Still possible | Your code must |
|---|---|---|---|
| Read committed (default) | per statement | lost update on read-modify-write, write skew, phantoms | use atomic updates or `FOR UPDATE` |
| Repeatable read (= snapshot isolation) | per transaction | write skew | retry on serialization failure |
| Serializable (SSI) | per transaction + read tracking | nothing | retry on serialization failure |

Anomalies to name: dirty read, non-repeatable read, phantom, **lost update**, **write skew**.
Tools: `UPDATE … SET n = n + 1` (atomic), `SELECT … FOR UPDATE` (pessimistic), version column
(optimistic), `FOR UPDATE SKIP LOCKED` (work queues), unique and exclusion constraints (let the
database enforce the invariant), advisory locks. Deadlocks: lock in a consistent order; the database
detects and aborts one transaction; retry.

## 2. Indexes and query plans

B+tree: fan-out in the hundreds, 3–4 levels for a billion rows, leaves linked for range scans.
Composite index `(a, b, c)`: usable for a leftmost prefix; equality columns first, then one range or
sort column. Covering index (`INCLUDE`): index-only scan. Partial index (`WHERE status = 'open'`),
expression index (`lower(email)`). Other types: hash, GIN (arrays, JSONB, full text), GiST (ranges,
geo), BRIN (huge append-only tables), HNSW/IVF (pgvector).

Reading a plan (`EXPLAIN (ANALYZE, BUFFERS)`): scan types (seq, index, index-only, bitmap), join
types (nested loop: small outer side; hash: large unsorted; merge: sorted inputs), estimated vs actual
rows (misestimates cause most bad plans: `ANALYZE`, extended statistics), sorts and hashes spilling to
disk, buffers read. Costs of indexes: every write updates every index; random keys (UUIDv4) thrash
the cache: prefer time-ordered ids (UUIDv7, Snowflake).

## 3. SQL patterns

Top-N per group (`ROW_NUMBER`), running totals (`SUM() OVER`), previous row (`LAG`), anti-join
(`NOT EXISTS`), sessions (flag + running sum), conditional aggregates. Evaluation order:
FROM → WHERE → GROUP BY → HAVING → windows → SELECT → ORDER BY → LIMIT. Traps: `NOT IN` with NULL,
join fan-out before aggregation, `WHERE` on the outer side of a LEFT JOIN, `COUNT(col)` vs `COUNT(*)`.

## 4. Replication, sharding, and choosing a database

Single-leader replication: async (RPO = lag, stale replicas) vs sync/quorum commit (RPO 0, latency).
Application anomalies: read-your-writes, monotonic reads: route by LSN. Failover: promote, fence
the old primary, repoint clients; split brain is the risk. Backups: base backup + WAL archive =
point-in-time recovery; an untested restore is not a backup.

Sharding: by range (scans, hot spots) or hash (even, no scans); key = tenant or user so transactions
stay local; many virtual shards so that resharding moves shards, not keys. Before sharding: indexes,
read replicas, caching, partitioning, a bigger machine, archiving.

| Need | Pick | Why |
|---|---|---|
| relational OLTP up to a few TB | Postgres | features, extensions, one node goes far |
| global consistency, horizontal SQL | Spanner, CockroachDB, YugabyteDB | consensus per range, distributed transactions |
| huge key-value at predictable latency | DynamoDB, Cassandra/ScyllaDB, Bigtable | partitioned, tunable consistency, model queries first |
| analytics over billions of rows | ClickHouse, BigQuery, Snowflake, DuckDB | columnar, vectorised |
| cache, counters, rate limits | Redis/Valkey | in-memory data structures |
| search | OpenSearch/Elasticsearch | inverted index, relevance |
| lakehouse | Parquet + Iceberg/Delta | snapshots, schema evolution, engines share one copy |

PACELC: under Partition choose Availability or Consistency; Else Latency or Consistency.
Postgres + async replicas PC/EL; Dynamo and Cassandra PA/EL by default; Spanner PC/EC.

## 5. Money and scarce things

Integer cents; append-only double-entry ledger (entries sum to zero; balances derived);
idempotency keys with a unique constraint in the same transaction; holds with expiry checked against
one clock; state machines for provider calls (PENDING → resolved by query/webhook); daily
reconciliation; sagas with compensations instead of distributed transactions.

## Questions

1. Which isolation level prevents write skew, and what does it cost?
<details><summary>Answer</summary>Serializable. Transactions can be aborted with serialization failures and must be retried; some extra tracking overhead.</details>

2. Index for `WHERE tenant_id = ? AND status = 'open' ORDER BY created_at DESC LIMIT 50`?
<details><summary>Answer</summary>(tenant_id, status, created_at): two equalities then the sort column; or a partial index on (tenant_id, created_at) WHERE status = 'open'.</details>

3. Estimated rows 10, actual rows 2,000,000 in a plan. What happened and what do you do?
<details><summary>Answer</summary>Stale or missing statistics, or correlated columns. ANALYZE, raise the statistics target, create extended statistics; the planner then stops choosing a nested loop.</details>

4. What is the RPO of async replication, and how do you get zero?
<details><summary>Answer</summary>The replication lag at the moment of failure. Zero needs synchronous (quorum) commit to at least one other node.</details>

5. Why not `balance = balance - amount` in a single column?
<details><summary>Answer</summary>No history, no audit, no way to detect or repair corruption. Use an append-only double-entry ledger; keep the balance as a derived cache.</details>
