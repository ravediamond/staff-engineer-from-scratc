# Week 6: RAG at staff level

You already ship RAG. This week makes you able to **defend every design choice with a
number** and to see the failure modes before users do: chunking that loses context, retrieval
that misses identifiers, metrics that flatter, indexes that go stale, ACLs that leak, answers
that cite nothing. Each lab is a piece of a production RAG stack you could drop into your own
eval harness.

Primer: `knowledge/06-rag.md`.

| Day | Lab | Review bug |
|---|---|---|
| d1 | chunking: fixed with overlap, recursive, heading-aware, spans back to source | stride = size + overlap leaves gaps |
| d2 | hybrid retrieval: BM25 + hashed dense + RRF + score fusion | RRF uses scores instead of ranks |
| d3 | retrieval metrics (recall, MRR, nDCG) + reranking + bootstrap CI | IDCG computed from the retrieved list |
| d4 | freshness: versioned index, CDC events, out-of-order safety | older update overwrites newer |
| d5 | ACL pre-filtering, citation checking, abstention, cost + **Friday design** | ACL post-filter after top-k |
