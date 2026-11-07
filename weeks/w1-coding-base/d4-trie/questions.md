# Questions

1. Trie vs hash set for "is this word in my dictionary": when does the trie win?
2. Two ways to serve top-k suggestions per prefix. Costs of each.
3. Design typeahead for 1B queries/day, p99 < 50 ms. What is precomputed, what is computed at request time?
4. How do you keep a newly trending query from waiting a day for the offline job?
5. Memory of a dict-of-dicts trie is too big. Name two compression techniques.

## Model answers

1. When you need prefix queries (autocomplete, longest-prefix match for routing tables, "any word starting with…"). For exact membership only, a hash set is simpler and usually faster.
2. DFS the prefix subtree at query time: small memory and cheap updates, but query cost is the subtree size, which is huge for short prefixes like "a". Cache top-k at each node: O(len + k) query, k entries of memory per node, and inserts must update k-lists along the path.
3. Offline daily job: count queries (with decay), filter, compute top-k per prefix up to length about 20, write to a sharded KV store keyed by prefix. At request time: KV lookup (~1 ms), merge with a small trending/real-time list, personalization re-rank on a few dozen candidates, safety filter. Client side: debounce and cache prefix results in the browser.
4. A streaming layer: a sliding-window counter (Count-Min sketch per minute) flags queries whose rate jumps far above baseline, and keeps a small trending top-k per prefix in memory, merged at serve time. Moderation gates trending entries.
5. Radix (Patricia) tree: collapse single-child chains into one edge labelled with a string. Or a succinct/array encoding: DAWG/minimal automaton sharing suffixes, double-array tries, or FSTs (Lucene stores its term dictionary as an FST).
