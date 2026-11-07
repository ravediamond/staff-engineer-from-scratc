# Week 3: distributed primitives

System design interviews at staff level are won or lost on whether you can reason about
partial failure precisely: what happens when this node is slow, that link drops, this clock is
wrong. This week builds the five primitives under every distributed store, queue and training
cluster: partitioning, replication, ordering, consensus, and leases. Each lab has a failure
injector in its tests: the point is to watch the primitive survive the failure.

Primer: `knowledge/03-distributed-systems.md`.

| Day | Lab | Review bug |
|---|---|---|
| d1 | consistent hashing, virtual nodes, rendezvous | ring lookup has no wrap-around |
| d2 | quorum replication (N, R, W), read repair | read returns first response, not newest |
| d3 | Lamport and vector clocks, sibling detection | merge keeps the "bigger" clock instead of element-wise max |
| d4 | Raft log replication and commit rule | commits entries from a previous term by counting (Figure 8) |
| d5 | leases and fencing tokens | storage does not remember the highest token |
