# Questions

1. B-tree vs LSM-tree: write path, read path, space, and which workloads favour each.
2. Why does a B+tree keep values only in leaves and link the leaves?
3. Composite index column order: state the rule and apply it to `WHERE tenant_id = ? AND created_at > ? ORDER BY created_at DESC LIMIT 20`.
4. What is a covering index, and what does it cost?
5. A query is slow. Walk through how you read `EXPLAIN (ANALYZE, BUFFERS)` and the five most common causes.
6. When do indexes hurt? Give four cases.

