# W6 D2: hybrid retrieval and fusion

Primer: `knowledge/06-rag.md` §2. Builds on W4 D3 (BM25) and W4 D4 (vector search).

## The one idea

Lexical (BM25) and dense retrieval fail on **different** queries: BM25 on paraphrases, dense on
identifiers and rare terms. Combining them almost always beats either alone. Two fusion families:

**Reciprocal Rank Fusion** (Cormack et al., 2009): uses only **ranks**, so score scales do not matter.
```
RRF(d) = Σ_{lists L containing d}  1 / (k + rank_L(d))      rank starts at 1, k = 60 by convention
```

**Score fusion:** normalise each list's scores to [0, 1] (min-max), then a weighted sum. Sensitive to
outliers and to the shape of each score distribution, but tunable.

Today's dense side is a **hashed bag-of-words embedding** (the "hashing trick"): deterministic, no
model download, and good enough to make fusion visible. In production, swap in a real encoder.

## Today's build (`w6d2_hybrid.py`)

`hash_embed(text, dim)` (unigrams + bigrams, signed hashing, L2-normalised), `rrf(rankings, k)`,
`minmax_fuse(score_dicts, weights)`, `HybridIndex(docs).search(query, k, mode)` with modes
`"bm25" | "dense" | "rrf"`. A small BM25 is provided, already written.

## Staff angle

Fusion is a place where teams fool themselves: they tune weights on 20 queries and ship. A staff
engineer insists on a held-out query set, reports per-slice results (identifier queries vs
natural-language queries), and treats RRF as the default precisely because it has almost
nothing to overfit. Then a cross-encoder reranker on the fused top-50 (D3) usually buys more
than any fusion tuning.
