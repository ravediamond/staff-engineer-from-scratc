# Questions

1. Why write to a log before applying the change? What does fsync buy and cost?
2. LSM vs B-tree: write amplification, read amplification, space amplification. When does each win?
3. Why are deletes tombstones in an LSM, and when can a tombstone be dropped?
4. Why must the SSTable be durable before truncating the WAL?
5. A vector DB's ingestion throughput collapses as the collection grows. Three hypotheses from today's material.

