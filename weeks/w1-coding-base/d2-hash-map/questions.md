# Questions

1. Why can't open addressing simply empty a slot on delete? Draw the failing case.
2. Chaining vs open addressing: when would you pick each? Mention memory and cache behaviour.
3. What is hash flooding and how do modern languages defend against it?
4. Your service's p99 latency doubles every few hours and drops after a restart. The hot path is a giant in-process dict with frequent inserts and deletes. Hypothesis and how you test it.
5. Python dicts keep insertion order. How, given they are hash tables?

## Model answers

1. `get` stops at the first empty slot. If A, B, C all start at slot 3 and sit at 3, 4, 5, emptying slot 4 makes `get(C)` stop at 4 and wrongly report "missing". A tombstone says "keep walking" to searches but "reusable" to inserts.
2. Chaining: simple deletes, graceful at high load, good when values are big or the map gets iterated rarely. Open addressing: one flat array, no per-entry allocation, far better cache locality, so faster at moderate load. It needs tombstones and careful resizing. Most high-performance maps (SwissTable, CPython) are open addressing.
3. An attacker sends keys that all collide, so every operation degrades to O(n) and a few KB of POST data can pin a CPU (2011 advisories). Defense: keyed hash functions with a per-process random seed (SipHash in Python, Rust, Ruby), plus input size limits.
4. Tombstone accumulation: deletes leave tombstones, probe chains lengthen, and a restart rebuilds the dict clean. Test: track `len(d)` against operation counts, microbenchmark lookups as delete churn grows, compare with a dict periodically rebuilt via `dict(d)`. CPython does rebuild on resize, but if the size oscillates below the resize threshold, chains can stay long. Fix: periodic rebuild or a different structure.
5. CPython splits storage: a dense `entries` array in insertion order plus a sparse `indices` hash table that stores positions into `entries`. Iteration walks `entries`, and the table also uses less memory than before (Raymond Hettinger's compact dict, 3.6).
