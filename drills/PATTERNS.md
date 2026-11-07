# Patterns, one line each (say the trigger, then the pattern)

| Trigger in the problem | Pattern | Typical complexity |
|---|---|---|
| "group / count / seen before" | hash map keyed by a canonical form | O(n) |
| "subarray sum equals / divisible by" | prefix sums + hash map of counts | O(n) |
| "longest/shortest contiguous … with constraint" | sliding window with a validity invariant | O(n) |
| "pair in sorted array", "maximise area between ends" | two pointers moving inward | O(n) |
| "next greater / warmer / smaller" | monotonic stack of indices | O(n) |
| nested brackets, expressions | stack (of counts, strings, operands) | O(n) |
| "minimum X such that feasible" | binary search on the answer + greedy feasibility check | O(n log range) |
| "k-th / top-k / merge sorted" | heap of size k | O(n log k) |
| "connected / same group" | union-find with path compression | ~O(n α(n)) |
| "order with prerequisites" | topological sort (Kahn), detect cycles | O(V + E) |
| "shortest path, ≤ k edges" | Bellman-Ford limited to k rounds (copy per round) | O(k·E) |
| "all combinations / placements" | backtracking with pruning | exponential, prune early |
| "number of ways / best value over prefixes" | 1-D DP, define dp[i] in one sentence first | O(n) or O(n·k) |
| "grid paths / two strings" | 2-D DP, often reducible to 1-D | O(m·n) |
| "can you reach / minimum jumps" | greedy with a frontier | O(n) |
| tree "per level" | BFS with a queue, process level by level | O(n) |
| tree "validity / path property" | DFS carrying bounds or state down, results up | O(n) |
| "design X with O(1) ops" | combine hash map + linked list / buckets | O(1) amortised |
| "median of a stream / window" | two heaps (lazy deletion for windows) | O(log n) per op |

**Staff habit:** before coding, say the invariant of your loop out loud. If you cannot, you do not have
the solution yet.
