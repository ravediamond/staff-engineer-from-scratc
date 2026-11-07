# W6 D3: retrieval metrics, reranking, confidence intervals

Primer: `knowledge/06-rag.md` §3 and `knowledge/07-evaluation-and-experimentation.md` §2.

## The one idea

| Metric | Formula (per query) | Answers |
|---|---|---|
| recall@k | relevant ∩ top-k / relevant | "did we retrieve the evidence at all?" (what RAG needs most) |
| precision@k | relevant ∩ top-k / k | "how much noise goes into the context?" |
| MRR | 1 / rank of first relevant (0 if none in list) | "how high is the first good hit?" |
| nDCG@k | DCG@k / IDCG@k, DCG = Σ (2^rel − 1) / log2(i + 1), i from 1 | graded relevance, position-weighted |

**IDCG is the DCG of the ideal ranking of all judged relevant documents**, not of the documents you
happened to retrieve. Compute IDCG from the retrieved list and every system gets nDCG ≈ 1.

Means over 50–200 queries are noisy. Report a **bootstrap CI over queries** (resample queries with
replacement, recompute the mean, take percentiles). Comparing two systems: **paired** bootstrap on
per-query differences (W7 D3).

**Reranking:** take the top-N from a cheap retriever, rescore with an expensive scorer
(cross-encoder), keep the top-k. Today the scorer is a function you pass in.

## Today's build (`w6d3_metrics.py`)

`recall_at_k`, `precision_at_k`, `reciprocal_rank`, `ndcg_at_k(retrieved, qrels_graded, k)`,
`rerank(candidates, scorer, k)`, `evaluate(run, qrels, k, n_boot, seed) -> {metric: (mean, lo, hi)}`.

## Staff angle

The staff move is to separate **retrieval quality** from **answer quality**, measure both, and
know which one is the bottleneck before spending a quarter on it. If recall@20 is 0.95 and answers
are still wrong, more retrieval work is wasted: the problem is generation, context assembly, or the
question set. If recall@20 is 0.6, no prompt engineering will fix it.
