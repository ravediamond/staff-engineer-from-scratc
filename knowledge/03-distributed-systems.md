# 03. Distributed systems

## §1 Partitioning

Hash partitioning (even spread, no range scans), range partitioning (range scans, hot spots on
sequential keys), consistent hashing with virtual nodes (minimal movement), rendezvous hashing.
Hot keys need replication, salting or caching, not better hashing.

## §2 Replication

Single-leader (simple, writes bottleneck at the leader, failover is the hard part), multi-leader
(multi-region writes, conflicts), leaderless quorums (N, R, W; R + W > N overlaps; sloppy quorums break it).
Replication lag gives read-your-writes and monotonic-read anomalies; fix with sticky reads or version tokens.

## §3 Time and ordering

Wall clocks skew; Lamport clocks give a causal-consistent total order; vector clocks detect concurrency.
Spanner's TrueTime bounds uncertainty and commit-waits. Hybrid logical clocks (HLC) combine physical
time with a logical counter (CockroachDB).

## §4 Consensus

Raft/Paxos: a majority agrees on a log. 2f + 1 nodes tolerate f failures. Each write costs a majority
round trip. Uses: metadata, configuration, leader election, locks, small critical state. Not for bulk data.

## §5 Leases and fencing

Leases expire; clients cannot know they lost one (GC pauses). Fencing tokens checked by the resource
make it safe. Storage must reject lower tokens atomically.

## CAP and PACELC, said correctly

CAP: during a **partition**, choose consistency (refuse some requests) or availability (answer with possibly
stale data). PACELC adds: **else**, in normal operation, choose latency or consistency. Most "AP vs CP"
debates are really about the latency/consistency trade-off in normal operation.

## Consistency models, strongest to weakest (the ones you will name)

Linearizable (single-copy illusion, real-time order) → sequential → causal → read-your-writes / monotonic
reads (session guarantees) → eventual. Pick per feature: payments need linearizable; a like counter can be eventual.

## Questions

1. Explain linearizability to a product manager, and when it is worth paying for.
<details><summary>Answer</summary>"Once anyone sees a change, everyone sees it, and the system behaves as if there were a single copy." Worth it for money, inventory, unique usernames and locks, where two people must not both win. Not worth it for feeds, likes and analytics, where a second of staleness is invisible and the cost (latency, availability during partitions) is real.</details>

2. Design leader election for a set of agent workers. What breaks?
<details><summary>Answer</summary>Use a lease in a consensus-backed store (etcd/ZooKeeper) with a TTL; the holder renews; the others watch. What breaks: a paused leader still acting after its lease expired. Fix with fencing tokens on every side effect and leader-only actions checked against the current term. Also clock assumptions: rely on the store's TTL, not local clocks.</details>

3. Multi-region active-active for a user-settings service: how would you handle conflicts?
<details><summary>Answer</summary>Per-field last-writer-wins with hybrid logical clocks for low-stakes fields, CRDTs (sets, counters) where merge semantics exist, home-region ownership per user (writes routed to the home region, reads anywhere) for fields that must not conflict. Expose the conflict policy explicitly in the API.</details>

4. Why do 4-node clusters make little sense for Raft?
<details><summary>Answer</summary>A majority of 4 is 3, so it tolerates 1 failure, the same as 3 nodes, but with more replication cost and more chances of failure. Odd sizes (3, 5) maximize fault tolerance per node.</details>
