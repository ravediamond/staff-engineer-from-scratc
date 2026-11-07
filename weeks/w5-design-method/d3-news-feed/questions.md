# Questions

1. Push vs pull vs hybrid: cost of a post and cost of a read for each.
2. How do you pick the celebrity threshold? What metric would you watch?
3. A user follows a new account. Their feed should show its last 20 posts. What changes?
4. The feed must be ranked, not chronological. Sketch the pipeline and its latency budget.
5. What breaks first at 10× users, and what do you monitor?

## Model answers

1. Push: post costs O(followers) writes, read costs 1 inbox read (fast reads, expensive celebrity posts). Pull: post is 1 write, read costs O(following) fetches plus a merge. Hybrid: push for most authors, pull for the few high-follower ones at read time. Bounded both ways.
2. Pick it where push write cost and pull read cost balance. Set the threshold so that the p99 time to complete a fan-out stays under the freshness SLO (e.g. <5 s), and so that read-time merges stay under a cap (followed celebrities usually <100). Watch fan-out queue lag, p99 feed latency, and inbox write QPS.
3. Backfill at follow time: an async job pulls the account's recent posts into the follower's inbox (bounded at 20), or the read path treats newly followed accounts as "pull" for a while.
4. Candidate generation (inbox + celebrity pulls + recommendations, ~500 items, ~20 ms) → feature hydration (~20 ms) → lightweight ranker prunes to 100 → heavy ranker (~40 ms) → filters (integrity, diversity, dedupe) and blending (~10 ms), under ~100 ms total. Log impressions and engagement for training, and evaluate with online A/B tests.
5. Fan-out workers and inbox storage write throughput (celebrity bursts), then cache memory for hot outboxes, then ranking compute. Monitor fan-out lag, inbox store write latency, cache hit rate, ranker p99, and freshness (post-to-visible time).
