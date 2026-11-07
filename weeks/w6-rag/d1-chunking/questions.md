# Questions

1. Why keep character offsets on every chunk?
2. Fixed vs recursive vs heading-aware: when each?
3. How would you choose chunk size for a new corpus, concretely?
4. Your corpus is 40% tables (maintenance schedules, part lists). What do you do?
5. "Late chunking", "contextual retrieval", "parent-child chunks": what problem does each solve?

## Model answers

1. Offsets let you cite the exact passage, highlight it in the UI, dedupe overlapping hits, rebuild chunks under a new strategy without re-parsing, and debug misses ("the answer is at chars 1200–1300; which chunk had it, and where did it rank?").
2. Fixed: a baseline, or uniform unstructured text. Recursive: prose, emails, transcripts. Heading-aware: anything with structure (manuals, specs, wikis, legal), usually combined with a recursive second pass for long sections.
3. Build a labelled query set (100–300 real questions with relevant passages). Run a grid of sizes (200, 400, 800 tokens) × overlap (0, 10–20%) × strategy. Measure recall@k and nDCG with bootstrap CIs, plus answer quality on a subset. Pick the cheapest configuration inside the best CI, and check the cost (number of chunks).
4. Parse tables as tables: extract them structurally (layout parser), keep each table whole or row-group chunks with headers repeated in every chunk, serialize to markdown or "column: value" text for embedding, store the structured version for exact lookup (SQL or a tool), and route numeric questions to the structured path.
5. Late chunking: embed the whole document with a long-context encoder, then pool token embeddings per chunk, so chunks keep document context. Contextual retrieval (Anthropic, 2024): prepend an LLM-written sentence situating each chunk in its document before embedding and BM25, which reduces "orphan" chunks. Parent-child: retrieve small precise chunks, return their larger parent section to the LLM for context.
