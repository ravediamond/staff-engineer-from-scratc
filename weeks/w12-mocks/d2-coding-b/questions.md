# Questions

1. State and justify the Misra–Gries error bound.
2. Misra–Gries vs Count-Min sketch vs exact counting with sampling: trade-offs.
3. B2 on 10M words: bidirectional BFS and wildcard indexing. Explain both.

## Model answers

1. Each decrement step removes k + 1 units of count (k counters plus the dropped new item), so at most n/(k+1) decrement steps happen; each item's counter is reduced by at most the number of decrement steps, so it underestimates by at most n/(k+1), and any item with frequency above n/(k+1) must survive.
2. Misra–Gries: deterministic, k counters, underestimates, finds heavy hitters only (no arbitrary point queries). Count-Min: point queries for any item with overestimate bounded by εn with probability 1 − δ, mergeable, needs a heap for top-k. Sampling: simple, unbiased estimates with variance, misses rare items. Both sketches are mergeable across shards.
3. Bidirectional BFS expands from both ends and meets in the middle, visiting about b^(d/2) nodes on each side instead of b^d. Wildcard indexing precomputes buckets like "h*t" → [hit, hot, hat], so neighbours come from O(L) bucket lookups instead of 26·L candidate strings checked against the set.
