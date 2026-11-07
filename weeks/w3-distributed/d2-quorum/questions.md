# Questions

1. Why does R + W > N give "reads see the latest write"? Draw it for N=3.
2. Name three ways an R + W > N system can still return stale or lost data.
3. Read repair vs anti-entropy: what does each fix?
4. Pick N, R, W for (a) a feature store read 100k/s, written in hourly batches; (b) a user-settings store; (c) a session store where losing data is fine.
5. When do you stop using quorums and use consensus?

## Model answers

1. Write quorum W and read quorum R are subsets of N; if R + W > N they cannot be disjoint (pigeonhole), so at least one replica in every read set holds the latest acknowledged write, and the max-version rule returns it.
2. Last-writer-wins with clock skew (a later write gets a lower timestamp and loses). Sloppy quorums and hinted handoff: the write went to stand-in nodes outside the home set. Concurrent writes: LWW silently drops one. Failed writes that partially applied can surface later. Replica restored from an old backup without anti-entropy.
3. Read repair fixes stale replicas for keys that get read, cheap and on the hot path. Anti-entropy (Merkle tree comparison in the background) fixes keys nobody reads, which would otherwise diverge forever.
4. (a) N=3, R=1, W=3: batch writes can wait for all, reads must be fast and any replica is fresh after the batch completes. (b) N=3, R=2, W=2: read-your-writes, tolerates one failure. (c) N=2 or 3, R=1, W=1: fastest and most available, staleness acceptable.
5. When you need a single agreed order or a single winner: leader election, locks, unique constraints, counters that must not lose increments, config changes, metadata of a distributed filesystem or training cluster. Quorums give overlap, not agreement.
