# 06. Retrieval-augmented generation

## §1 Chunking

Fixed with overlap (baseline), recursive (prose), heading-aware (structured docs), parsers per document
family (tables, forms, scans). Keep offsets. Contextual retrieval and late chunking reduce orphan chunks.
Choose by evaluation, not taste.

## §2 Hybrid retrieval

BM25 + dense, fused with RRF (k = 60) or normalised score fusion. Query rewriting, HyDE and multi-query only
where measured. Multilingual: either multilingual embeddings or per-language pipelines; check analyzers.

## §3 Reranking and metrics

Cross-encoder reranker on the top 50–100. Metrics: recall@k (the bottleneck metric), precision@k, MRR,
nDCG with IDCG from all judgments. Paired bootstrap CIs over queries. Separate retrieval quality from answer quality.

## §4 Freshness

The index is a derived view. CDC or crawls feed version-checked upserts and versioned tombstones. Staleness is
a monitored metric; permission changes have a stricter SLA than content changes.

## §5 ACL, citations, abstention, cost

Pre-filter on ACL inside retrieval; re-check at answer time; missing ACL = nobody. Mandatory citations
verified by NLI or a judge. Abstain below a calibrated retrieval-confidence threshold. Cost is dominated by
LLM input tokens: rerank to fewer chunks, cache per permission group, route easy queries to small models.

## Where RAG systems fail (debug in this order)

1. The answer is not in the corpus (coverage) → ingestion/parsing.
2. It is in the corpus but not retrieved (recall) → chunking, hybrid, query handling.
3. Retrieved but ranked too low or cut by k (ranking) → reranker, k.
4. In context but ignored or misread (generation) → prompt, model, context order and length.
5. Correct but unhelpful (UX) → formatting, citations, follow-ups.

## Questions

1. RAG vs fine-tuning vs long context for a 5,000-document internal corpus: decide.
<details><summary>Answer</summary>RAG by default: documents change, permissions differ per user, citations are required, and cost scales with query, not corpus. Long context (stuffing everything) when the corpus is small enough per query and changes rarely (with prompt caching). Fine-tuning for style, format or domain language, not for facts that change. Often RAG + a light fine-tune for the answer format.</details>

2. How do you evaluate a RAG system end to end without labelling everything?
<details><summary>Answer</summary>A labelled core set (200–500 questions with gold passages and reference answers, sliced), retrieval metrics on it, an answer-level LLM judge calibrated against humans, citation-support checks on all answers, and online signals (thumbs, escalations, click-through on citations). Grow the labelled set from production failures.</details>

3. Agentic RAG (the model decides when and what to retrieve, multiple hops): when is it worth it?
<details><summary>Answer</summary>For multi-hop questions (compare, aggregate, chains of lookups) and heterogeneous sources (docs + SQL + APIs). It costs latency, money and evaluation difficulty (trajectories, not single retrievals). Route only the queries that need it; measure per-slice gains against a single-shot baseline.</details>
