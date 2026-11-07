# Questions (out loud, 1–2 minutes each)

1. Why is bottom-up heapify O(n) when n pushes are O(n log n)? Give the intuition, not the proof.
2. Top-k largest of a stream: why a min-heap? What changes for top-k smallest?
3. Your top-k service runs on 1,000 shards, each with 10M items. Design the query path. What crosses the network?
4. When would you not use a heap for top-k at all?
5. `heapq` stores `(priority, item)`. Two equal priorities and items that are not comparable: what breaks, and the standard fix?

## Model answers

1. Most nodes are near the bottom and sift down only a few levels: half are leaves (0 work), a quarter sift ≤1 level, an eighth ≤2… The total is a geometric sum bounded by ~n swaps (≤2n comparisons). Pushes go the other way: each new leaf may climb log n levels, and in the worst case (decreasing input) all of them do.
2. The root of a min-heap is the weakest of the current top k, the one to evict. Compare each new item to it in O(1) and replace in O(log k). For top-k smallest, keep a max-heap of size k (push negated values in Python).
3. Each shard computes its local top-k (k·log k per shard, in parallel) and returns k items; the aggregator merges 1,000 lists of k with a heap: k·1,000 items cross the network, not 10^10. If k is large, use a k-way merge that pulls lazily, or a two-round threshold algorithm (Fagin/TA style) to stop early.
4. One-shot on in-memory data: quickselect, O(n) average (`np.partition`). Top-k frequent under memory limits: a sketch (Count-Min + small heap, or Misra-Gries). Data already sorted or indexed: just read the first k.
5. On a priority tie, Python compares the items and raises `TypeError` (or orders by something meaningless). Push `(priority, counter, item)` with a monotonically increasing counter: it breaks ties and also makes order FIFO among equal priorities (stable).
