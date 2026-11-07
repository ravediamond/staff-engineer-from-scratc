# Questions

1. What does "committed" mean in Raft, and when can a client be told "success"?
2. Explain the log-matching check. Why `prev_index` and `prev_term`?
3. Why can't the leader commit an old-term entry just because a majority stores it? (Figure 8, in words.)
4. 3 or 5 nodes for the metadata store of a 2,000-GPU training cluster? Cross-zone or cross-region?
5. Consensus is slow. Name three ways real systems reduce its cost.

## Model answers

1. Stored on a majority by the leader of the entry's term (or covered by a later committed entry), so any future leader must have it (election restriction). The client hears success after the leader applies it to its state machine once committed.
2. If a follower has an entry at prev_index with prev_term, then by induction its whole log up to there matches the leader's (Log Matching Property). A mismatch means divergence earlier, so the leader backs up next_index until it finds the agreement point, then overwrites from there.
3. An old-term entry on a majority can still be overwritten. A server holding a different entry at that index with a higher term can win an election, because voters compare last-log term first, and erase it. Committing only current-term entries by counting guarantees any future leader's log contains them. Older entries commit implicitly with them.
4. Five nodes across three zones: survive one zone loss plus one more node, at the cost of a slightly slower majority. Stay in one region: cross-region consensus adds 100+ ms per write and the training cluster sits in one region anyway. Keep it a metadata store (job state, membership, checkpoints manifest), never the data path.
5. Batching and pipelining many entries per round trip; leader leases for local linearizable reads without a quorum round; multi-Raft (thousands of small groups, one per shard, to spread leadership); follower reads with read-index; witness or non-voting replicas; Flexible Paxos quorums.
