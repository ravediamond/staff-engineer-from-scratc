# Questions

1. Why not order events by wall-clock timestamps?
2. Lamport vs vector clocks: what can a vector clock tell you that Lamport cannot?
3. What does a store do with concurrent versions? Give two real strategies.
4. Vector clocks grow with writers. How do production systems bound them, or avoid them?
5. Google Spanner uses wall clocks for ordering. How does it get away with it?

## Model answers

1. Clocks skew (ms to s), jump (NTP corrections, VM migration), and leap-smear. A later write can get an earlier timestamp and silently lose under last-writer-wins. Causality, not physical time, is what correctness usually needs.
2. Lamport gives a total order consistent with causality, but `L(a) < L(b)` does not imply causality. Vector clocks characterise causality exactly: a → b iff VC(a) < VC(b), and incomparable means concurrent, so they detect conflicts.
3. Keep siblings and let the application or user merge on read (Dynamo shopping cart: union, with deletes needing tombstones), or use CRDTs that merge deterministically (G-counters, OR-sets, sequence CRDTs for text). Last-writer-wins also exists but drops data.
4. Prune old entries (risking false conflicts), use dotted version vectors keyed by server rather than client (Riak), or design around them: single leader per partition, or CRDTs.
5. TrueTime exposes clock uncertainty as an interval [earliest, latest] (GPS + atomic clocks keep ε ≈ 1–7 ms). Commit-wait: a transaction waits out the uncertainty before its timestamp becomes visible, so timestamp order matches real-time order (external consistency). It buys correctness with hardware and a few ms of latency.
