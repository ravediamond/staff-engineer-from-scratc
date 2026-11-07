# Week 1: coding base and communication

Staff loops at Google and Meta still have two coding rounds. They are not easier at staff level;
the bar shifts from "solved it" to "solved it cleanly, said the invariant, tested it, talked like
someone I want next to me in an incident". This week rebuilds the five structures that show up
inside half of all interview problems, from scratch, with invariants spoken out loud.

Primer: `knowledge/01-python-for-interviews.md` (2h day or weekend).

| Day | Lab | Review bug |
|---|---|---|
| d1 | binary heap, heapify, top-k | sift-down always picks the left child |
| d2 | open-addressing hash map | delete without tombstone breaks probe chains |
| d3 | LRU and TTL cache, O(1) | `get` does not refresh recency |
| d4 | trie and top-k autocomplete | a word that is a prefix of another is never marked |
| d5 | intervals: merge, insert, booking, sweep line | merge sorts by end, not start |
