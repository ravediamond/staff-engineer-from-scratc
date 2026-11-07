# W3 D1: consistent hashing

Primer: `knowledge/03-distributed-systems.md` §1.

## The one idea

`node = hash(key) % N` moves almost every key when N changes (going from 10 to 11 nodes moves
~91% of keys). **Consistent hashing** places nodes and keys on the same ring of hash values;
a key belongs to the first node clockwise. Adding a node only steals keys from its successor:
about **1/(N+1)** of keys move.

Problem: with one point per node, arcs are uneven (max/mean load ~ log N / log log N).
**Virtual nodes**: each physical node owns V points (`hash(f"{node}#{i}")`). Load evens out roughly
as `1 ± 1/sqrt(V)`, and when a node leaves, its load spreads over many nodes instead of one.

**Rendezvous (highest random weight) hashing**: for each key, pick `argmax_node hash(node, key)`.
No ring, no vnodes, perfect minimal movement, O(N) per lookup (fine for N < ~100 or with a
cached result). Used for picking replicas in many systems (e.g. it is how some CDNs pick caches).

**Invariant (ring):** the points list is sorted; lookup = first point with `hash >= h(key)`,
**wrapping to index 0** past the end.

## Today's build (`w3d1_hashing.py`)

- `stable_hash(s) -> int` (MD5, first 8 bytes: Python's `hash()` is salted per process).
- `Ring(vnodes)`: `add(node)`, `remove(node)`, `lookup(key)`, `assignment(keys) -> dict`.
- `moved_fraction(a, b)` between two assignments.
- `rendezvous(key, nodes)`.
- `max_over_mean(assignment)` load imbalance.

## Staff angle

Consistent hashing solves movement, not **hot keys**: one celebrity key still lands on one node.
Staff answers add: replication of hot keys (read from any of k replicas), key salting (`key#0..k`
for writes that can be split), request coalescing, or a dedicated cache tier. And for stateful
ML serving (KV-cache-aware routing in LLM serving), the same ring idea routes requests with a
shared prefix to the same replica, so the prompt cache hits: consistent hashing on the prefix.
