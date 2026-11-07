# Questions (out loud, 1–2 minutes each)

1. Why is bottom-up heapify O(n) when n pushes are O(n log n)? Give the intuition, not the proof.
2. Top-k largest of a stream: why a min-heap? What changes for top-k smallest?
3. Your top-k service runs on 1,000 shards, each with 10M items. Design the query path. What crosses the network?
4. When would you not use a heap for top-k at all?
5. `heapq` stores `(priority, item)`. Two equal priorities and items that are not comparable: what breaks, and the standard fix?

