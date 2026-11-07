# W4 D1: write-ahead log and LSM tree

Primer: `knowledge/04-storage-and-retrieval.md` §1.

## The one idea

**Write-ahead log:** before changing any in-memory state, append the change to a log on disk.
After a crash, replay the log. A crash can tear the last record in half, so replay must ignore
a corrupt **tail** record (and only the tail).

**LSM tree** (LevelDB, RocksDB, Cassandra, and the storage engine under many vector DBs):

```
put/delete ──▶ WAL (append) ──▶ memtable (dict, in RAM)
                                   │ when full: flush as a sorted immutable file
                                   ▼
                     SSTables: [newest] [older] [oldest]   (compaction merges them, D2)
get(key): memtable → newest SSTable → … → oldest. First hit wins. A tombstone hit means "deleted".
```

**Invariant:** for any key, the most recent write is found first in the search order. That is
the only reason a delete can be a tombstone instead of an in-place removal from older files.

Writes are sequential appends (fast on any disk); reads may touch several files (bloom filters
in D2 skip most of them). B-trees make the opposite trade.

## Today's build (`w4d1_lsm.py`)

- `WAL(path)`: `append(record: dict)` (one JSON line, flushed), `replay() -> list[dict]` (skips a torn last line), `truncate()`.
- `LSM(directory, memtable_limit)`: `put`, `delete`, `get`, automatic `flush()` to `sst-<n>.json` files when
  the memtable reaches the limit, and recovery: a new `LSM` on the same directory loads SSTables and replays the WAL.

## Staff angle

Write amplification (bytes written to disk / bytes written by the user) and read amplification
(files touched per read) are the two numbers that decide storage engines. A staff answer to
"why is our vector DB ingestion slow?" goes: what is the compaction policy, what is write amp
right now, are we flushing tiny segments because of a refresh interval? That is exactly the
Elasticsearch / Lucene segment-merge story, and the Milvus / Qdrant segment story.
