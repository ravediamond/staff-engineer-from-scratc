# 01. Python for coding interviews

## §1 Complexity cheat sheet (CPython)

| Operation | Cost | Note |
|---|---|---|
| `list.append`, `list.pop()` | O(1) amortised | `pop(0)` and `insert(0, x)` are O(n): use `collections.deque` |
| `x in list` | O(n) | `x in set` / `dict` is O(1) average |
| `list.sort()`, `sorted()` | O(n log n) | Timsort, stable, O(n) on already-sorted runs |
| `heapq.heappush/pop` | O(log n) | min-heap only; negate for max-heap |
| `heapq.heapify` | O(n) | bottom-up |
| `bisect.bisect_*` | O(log n) | `insort` is O(n) because of the list shift |
| string `+=` in a loop | O(n²) worst | build a list and `"".join` |
| `dict` iteration order | insertion order | guaranteed since 3.7 |

Recursion limit is ~1000 frames: deep DFS on 10⁵ nodes needs an explicit stack.

## §2 Heaps

Array-backed complete binary tree, children `2i+1, 2i+2`. Push = sift up, pop = swap root with last,
sift down choosing the **smaller** child. Heapify bottom-up is O(n). Top-k largest = min-heap of size k.
Ties with non-comparable payloads: push `(priority, counter, item)`.

## §3 Hash maps

Open addressing (CPython, SwissTable) vs chaining. Deletion needs tombstones; resize at load factor ~2/3.
Adversarial keys → hash flooding; seeded hashes defend. `hash(1) == hash(1.0) == hash(True)`.

## §4 LRU

Dict + doubly linked list with sentinels; `OrderedDict.move_to_end` in production code. Policy matters
more than structure: scans pollute LRU (use 2Q/ARC/TinyLFU).

## §5 Tries

Prefix queries in O(len). Real systems precompute top-k per prefix and serve from a KV store. Compress
with radix trees or FSTs.

## §6 Intervals

Sort by start, one pass. Half-open `[s, e)`: at equal times process ends before starts. Peak concurrency
= sweep line. Calendar insertion = bisect neighbours.

## Python gotchas interviewers notice

- Mutable default arguments (`def f(x=[])`).
- `is` vs `==` (only use `is` for `None` and sentinels).
- Integer division and negative numbers: `-7 // 2 == -4`, `int(-7 / 2) == -3`.
- `copy` vs `deepcopy` for nested lists (`[[0] * n] * m` aliases rows).
- Generators are single-use.

## Questions

1. Why is `collections.deque` the right queue, and when is `queue.Queue` right instead?
<details><summary>Answer</summary>deque gives O(1) appends and pops at both ends and is thread-safe for single append/pop calls; it has no blocking. `queue.Queue` adds locks, blocking get/put with timeouts and maxsize, for producer/consumer threads. In asyncio use `asyncio.Queue`.</details>

2. Your solution is O(n log n). The interviewer asks for O(n). What patterns do you reach for?
<details><summary>Answer</summary>Hashing (replace sorting-based grouping or lookup), counting sort or bucketing when values are bounded, monotonic stacks or deques for next-greater and window problems, two pointers on data that is already sorted, prefix sums, quickselect for order statistics, and union-find for connectivity.</details>

3. When does Python's speed actually matter in an interview?
<details><summary>Answer</summary>Rarely for correctness, but O(n²) on 10⁵ elements (10¹⁰ ops) will not finish, while O(n log n) on 10⁶ is fine. Say the expected input size, pick the complexity accordingly, and mention constant factors (dict lookups vs list indexing) only if asked.</details>

4. How do you test your code in a whiteboard round without running it?
<details><summary>Answer</summary>Walk one normal example line by line with variable values, then edge cases (empty, one element, duplicates, negative values, maximum size), and check the loop invariant at entry, each iteration and exit. Say what a property-based test would check.</details>
