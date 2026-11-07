# Questions

1. Why write to a log before applying the change? What does fsync buy and cost?
2. LSM vs B-tree: write amplification, read amplification, space amplification. When does each win?
3. Why are deletes tombstones in an LSM, and when can a tombstone be dropped?
4. Why must the SSTable be durable before truncating the WAL?
5. A vector DB's ingestion throughput collapses as the collection grows. Three hypotheses from today's material.

## Model answers

1. So that every acknowledged change survives a crash: replay rebuilds memory state. fsync makes the bytes durable on the device rather than in the OS page cache. It costs a disk flush (ms on SSD, more on network disks), which is why systems group-commit many writes per fsync.
2. LSM: sequential writes and high ingest, but reads may check several runs and compaction rewrites data (write amp 10–30× over time); wins for write-heavy workloads and time series. B-tree: in-place updates, one root-to-leaf read path; wins for read-heavy, range-scan workloads with updates. Space: LSMs hold obsolete versions until compaction.
3. Older SSTables are immutable and may still hold the key; without a tombstone that is found first, the old value would reappear. It can be dropped once compaction reaches the oldest level containing that key (no older version can exist below), and after any replication grace period.
4. Otherwise a crash between "truncate WAL" and "SSTable on disk" loses acknowledged writes. Order: write a temp file, fsync, atomic rename, then truncate.
5. Too-frequent flushes creating many small segments, so read and merge amplification grows. Compaction or segment merges falling behind, so writes stall (RocksDB write stalls). Index building (HNSW insertion) cost growing with segment size, plus a missing bulk-load path.
