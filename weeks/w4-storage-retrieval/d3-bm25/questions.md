# Questions

1. Walk through the BM25 formula: what do IDF, k1 and b each control?
2. Why intersect postings from the shortest list?
3. BM25 vs dense retrieval: name query types where each wins.
4. How would you shard an inverted index over 1B documents? Document-partitioned vs term-partitioned.
5. Your French technical corpus gets poor BM25 results. What do you check first?

## Model answers

1. IDF weights rare terms up and common terms down. k1 controls tf saturation: higher k1 means more credit for repeats. b controls length normalization: 0 is none, 1 is full division by relative length. The denominator `tf + k1(1-b+b·|D|/avgdl)` makes long documents need more occurrences for the same score.
2. The intersection can only be as large as the smallest list. Walking it and probing the others (or skipping with skip lists) costs about O(min_len · log), not the sum of all lengths.
3. BM25 wins on exact identifiers, error codes, rare names, out-of-domain jargon and new vocabulary. Dense wins on paraphrase, synonyms, natural-language questions phrased unlike the document, and cross-lingual queries. That is why production uses hybrid.
4. Document-partitioned (each shard indexes a subset of docs; queries fan out to all shards and merge top-k): standard, balanced, simple to update. Term-partitioned (each shard owns some terms' full postings): fewer shards per query but hot terms create hotspots and multi-term queries ship postings across the network. Almost everyone uses document partitioning with replicas.
5. The analyzer: accent folding (é→e), elision ("l'pompe" → "pompe"), lowercasing, a French stemmer (Snowball) or lemmatizer, compound and hyphenated technical tokens (E-4471, O2), stopwords. Then check BM25 parameters and field boosts (title vs body). Measure on a labelled query set before and after each change.
