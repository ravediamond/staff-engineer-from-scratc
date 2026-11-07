# W6 D1: chunking

Primer: `knowledge/06-rag.md` §1.

## The one idea

Chunking decides what the retriever can ever find. A fact split across two chunks is
unretrievable as a whole; a chunk that mixes three topics has a blurry embedding.

| Strategy | How | Good for | Bad at |
|---|---|---|---|
| Fixed size + overlap | windows of `size` chars, stride `size - overlap` | baselines, uniform text | cuts mid-sentence, mid-table |
| Recursive | split on the strongest separator that works (`\n\n`, `\n`, `. `, ` `), merge pieces up to `max_len` | prose | structure-blind |
| Heading-aware | split on headings, keep the heading path as metadata | manuals, docs, wikis | very long sections need a second pass |

**Invariant:** every chunk keeps `(start, end)` offsets into the source text, and chunks
**cover the source with no gaps**. Offsets are how citations point back to the exact passage
(D5), and how you debug "why didn't we retrieve this?".

## Today's build (`w6d1_chunking.py`)

`fixed_spans(text, size, overlap)`, `recursive_spans(text, max_len, seps)`,
`heading_chunks(markdown) -> [{"path", "start", "end"}]`, `to_records(doc_id, text, spans)`.

## Staff angle

Chunking is an **eval question**, not a taste question. A staff engineer sets up the grid
(strategy × size × overlap) against a labelled query set and reports recall@k with confidence
intervals (D3), then also checks cost (more chunks = more embeddings and storage) and answer
quality downstream. And for structured documents (tables, forms, P&IDs at an industrial
company) the right answer is often a parser per document family, not a smarter splitter.
