# Questions

1. Give the logical evaluation order of a SELECT statement and two consequences.
2. `ROW_NUMBER`, `RANK`, `DENSE_RANK`: difference on ties, and which one for "top 3 per group"?
3. Why is `NOT IN` dangerous, and what do you write instead?
4. A dashboard's revenue doubled after someone joined a second table. Explain the mechanism and the fix.
5. Normalised (3NF) vs denormalised vs star schema: where do you use each?
6. OLTP row store vs OLAP column store: why is each fast at what it does? Name two of each.

## Model answers

1. FROM and JOINs → WHERE → GROUP BY → HAVING → window functions → SELECT list → DISTINCT → ORDER BY → LIMIT. Consequences: a column alias from SELECT cannot be used in WHERE; window functions cannot be filtered in WHERE or HAVING (use a CTE); WHERE filters rows before aggregation and HAVING filters groups after; a WHERE condition on the nullable side of a LEFT JOIN removes the unmatched rows.
2. On ties: ROW_NUMBER gives distinct consecutive numbers (arbitrary among ties unless the ORDER BY breaks them); RANK gives equal rows the same number and then skips (1, 1, 3); DENSE_RANK does not skip (1, 1, 2). Top 3 per group: ROW_NUMBER with a deterministic tie-breaker when you want exactly 3 rows; DENSE_RANK when you want every row within the three best values.
3. If the subquery returns any NULL, `x NOT IN (…)` is never TRUE and the query silently returns nothing. Write `NOT EXISTS (correlated subquery)`, or a LEFT JOIN with `WHERE right.key IS NULL`. Planners also handle NOT EXISTS as an anti-join more reliably.
4. Join fan-out: the grain changed. One order row matched N rows of the new table, so each order's amount was repeated N times before SUM. Fix: aggregate each child table to the parent's grain in a subquery/CTE before joining, or use `COUNT(DISTINCT …)` / window de-duplication when appropriate; state the grain of every table and of the result, and test totals against the base table.
5. 3NF for transactional systems: one fact in one place, writes are cheap and consistent. Denormalised (duplicated columns, materialised aggregates, document shapes) for read paths that need one lookup, at the price of keeping copies in sync. Star schema (a fact table at a declared grain plus dimension tables) for analytics: simple joins, columnar-friendly, slowly changing dimensions for history.
6. Row store: a whole row lives together, B-tree indexes find one row in a few page reads, MVCC and WAL give transactions: fast point reads and writes (Postgres, MySQL; Spanner/CockroachDB when distributed). Column store: each column is stored separately, sorted and compressed; a query reads only the columns it needs and processes them in vectorised batches, skipping blocks through min/max statistics: fast scans and aggregates over billions of rows, slow single-row updates (ClickHouse, BigQuery, Snowflake, DuckDB; Parquet as the file format).
