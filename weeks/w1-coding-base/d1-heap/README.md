# W1 D1: binary heap, heapify, top-k

Primer: `knowledge/01-python-for-interviews.md` §2. Drill pattern: `drills/PATTERNS.md` "heaps".

## The one idea

A binary heap is an array that pretends to be a complete binary tree. Node `i` has children
`2i+1`, `2i+2` and parent `(i-1)//2`. **Invariant (min-heap): `a[parent(i)] <= a[i]` for every `i > 0`.**
Every operation is "break the invariant in one place, then repair it along one root-to-leaf path":

| Operation | Breaks the invariant at | Repair | Cost |
|---|---|---|---|
| push | the new last leaf | sift **up** | O(log n) |
| pop | the root (last leaf moved there) | sift **down**, swap with the **smaller** child | O(log n) |
| heapify | everywhere | sift down every internal node, from the last one to the root | **O(n)**, not O(n log n) |

Why heapify is O(n): half the nodes are leaves (0 work), a quarter sift at most 1 level, an eighth
at most 2… The sum `n/4·1 + n/8·2 + n/16·3 + …` converges to `n`.

**Top-k largest of a stream**: keep a **min**-heap of size k. Its root is the smallest of your current
top k, the "bouncer": a new item enters only if it beats the bouncer. O(n log k) time, O(k) memory.
Interviewers love asking why it is a min-heap and not a max-heap.

## Narrate-while-coding protocol (use it every day from now on)

Staff coding rounds score communication as much as correctness. Say these five things, in order,
out loud, even alone:

1. **Restate + examples** (1 min): "So I get a stream and k, I return the k largest, sorted descending. Example: [5,1,9,3], k=2 → [9,5]. Edge: k=0, k > n, duplicates."
2. **Approach + complexity before code** (2 min): "Brute force is sort, O(n log n). Better: size-k min-heap, O(n log k), O(k) memory. I'll do that."
3. **Invariant** (1 sentence): "After processing i items, the heap holds the k largest of those i."
4. **Code, narrating intent not syntax**: "Now the repair step", not "now I write a while loop".
5. **Test by hand, then edge cases**: walk one example through the code, then empty / one item / duplicates.

## Today's build (`w1d1_heap.py`)

- `MinHeap`: `push`, `pop`, `peek`, `__len__`, with private `_sift_up` and `_sift_down`.
- `heapify(a)`: in place, bottom-up, O(n).
- `heap_sort(a)`: returns a new ascending list using your heap functions (no `sorted`, no `heapq`).
- `top_k_largest(stream, k)`: size-k min-heap, returns descending.

## Staff angle

A senior answers "use a heap". A staff engineer adds when not to: for a one-shot top-k on data that
fits in memory, `quickselect` is O(n) average; for top-k across 1,000 shards, each shard returns its
local top-k and you merge (k·shards items, not n). For a streaming top-k of *frequent* items under
memory limits, a heap is wrong: you need a sketch (Count-Min + heap, or Misra-Gries, see drill d07).
