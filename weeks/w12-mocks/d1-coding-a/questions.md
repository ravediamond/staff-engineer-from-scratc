# Questions (after the mock, out loud)

1. Prove the least_interval formula.
2. TimeMap: what if timestamps can arrive out of order? What if you need range queries?
3. How would you make TimeMap persistent and distributed for a feature store?

## Model answers

1. Let m be the max frequency and k the number of tasks with that frequency. The most frequent tasks need (m − 1) full cycles of length n + 1 plus a final partial cycle of the k max-frequency tasks: (m − 1)(n + 1) + k is a lower bound. Other tasks fill idle slots; if there are more tasks than slots, no idle time is needed and the answer is len(tasks). The answer is the max of both, and the greedy schedule achieves it.
2. Out of order: insert with `bisect.insort` (O(n) per insert in a list) or use a balanced tree / sorted container (O(log n)). Range queries: bisect both ends and slice. Many versions: periodic compaction, or a skip list.
3. Partition by entity key; store (key, ts) → value in an LSM-backed store sorted by key then timestamp (point-in-time get = seek to (key, ts) and step back); a TTL or compaction policy on old versions; online store for latest value, offline store (Parquet partitioned by date) for point-in-time-correct training joins; consistency between the two is the hard part.
