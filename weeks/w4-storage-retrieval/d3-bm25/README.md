# W4 D3: inverted index and BM25

Primer: `knowledge/04-storage-and-retrieval.md` §3. Used again in W6 D2 (hybrid retrieval).

## The one idea

An **inverted index** maps each term to its **postings**: the documents containing it, with term
frequency. Queries touch only the postings of query terms, not every document.

**BM25** (Robertson & Spärck Jones; Lucene/Elasticsearch default) scores a document D for query Q:

```
score(D, Q) = Σ_{t in Q}  IDF(t) · tf(t,D)·(k1 + 1) / ( tf(t,D) + k1·(1 - b + b·|D|/avgdl) )
IDF(t)      = ln( (N - df(t) + 0.5) / (df(t) + 0.5) + 1 )      (Lucene's always-positive variant)
```

- `k1` (~1.2–2.0) saturates term frequency: the 10th occurrence adds much less than the 1st.
- `b` (~0.75) normalises by length: a long document mentioning the term once is less relevant than a short one. `|D|/avgdl > 1` must **lower** the score.
- Rare terms (small df) get high IDF.

**Boolean AND**: intersect postings, starting from the **shortest** list (cost bounded by the rarest term).

BM25 is still a hard baseline in 2026: on keyword-heavy, ID-heavy or out-of-domain queries it often
beats dense retrieval, which is why production RAG is hybrid (W6 D2).

## Today's build (`w4d3_bm25.py`)

`tokenize(text)` (lowercase, `[a-z0-9]+`), `InvertedIndex.add(doc_id, text)`, `df(term)`, `avgdl`,
`bm25(query, k=10, k1=1.5, b=0.75) -> [(doc_id, score)]` sorted by score desc then doc_id asc, and
`search_and(query) -> sorted doc ids`.

## Staff angle

When a RAG system misses "error code E-4471", the staff engineer's first question is "is there a
lexical channel?" Dense embeddings blur exact identifiers, part numbers and rare names. The
second question is about the tokenizer: BM25 with a bad tokenizer (no handling of `E-4471`, no
stemming for the language, no accent folding for French) is a broken baseline, and broken
baselines make every new model look good.
