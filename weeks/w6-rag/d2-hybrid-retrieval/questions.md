# Questions

1. Why does hybrid retrieval beat either channel? Give a query type each channel fails on.
2. RRF vs min-max score fusion: trade-offs.
3. How do you tune fusion without overfitting?
4. Where does a reranker go, and what does it cost?
5. Query rewriting / HyDE / multi-query: when are they worth their latency?

## Model answers

1. Their errors are weakly correlated. BM25 fails on paraphrase and synonyms ("car won't start" vs "engine fails to ignite"). Dense fails on exact identifiers, rare names and new jargon ("E4471", "P-101"). Fusion recovers both.
2. RRF: rank-only, scale-free, robust, almost nothing to tune, but discards score magnitude (a 0.99 match and a 0.51 match at the same rank count the same). Min-max fusion keeps magnitudes and is tunable via weights, but is sensitive to outliers, to score-distribution shape and to the number of candidates; scores are not comparable across queries.
3. A held-out labelled query set, stratified by query type, with weights tuned on a dev split and reported on test with bootstrap CIs. Prefer RRF unless tuned fusion wins outside the CI. Re-check when the embedding model or corpus changes.
4. After fusion, on the top 50–100 candidates: a cross-encoder scores (query, chunk) pairs jointly. Cost is about 50 forward passes per query (~20–80 ms on GPU for a small reranker, or an API cost per query). It usually gives the largest single quality gain.
5. When queries are short or ambiguous, or phrased very unlike the documents (users ask questions, docs state facts), and recall is measured as the bottleneck. They cost one LLM call (100–500 ms) before retrieval. Gate them: apply only to queries the router flags, and measure the gain per slice.
