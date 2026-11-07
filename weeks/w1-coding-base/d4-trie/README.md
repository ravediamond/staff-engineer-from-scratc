# W1 D4: trie and top-k autocomplete

Primer: `knowledge/01-python-for-interviews.md` §5.

## The one idea

A trie stores strings by their characters along a path. Each node: `children: dict[char, Node]`,
`is_word: bool`, and whatever you need for the query (today: `count`, how often the word was
inserted). Lookup cost depends on the **key length**, not on how many words are stored.

**Invariant:** a word `w` is in the set iff walking `w` from the root ends at a node with
`is_word=True`. A path existing is not enough: `"car"` exists as a path inside `"cart"`.

**Autocomplete top-k** by frequency, two designs:

| Design | Query cost | Memory | Update cost |
|---|---|---|---|
| DFS the subtree at query time + heap | O(subtree) | small | O(len) |
| Cache top-k at every node (today, optional bonus) | O(len + k) | k entries per node | O(len · k) |

Real systems (Google search suggest) precompute top-k per prefix offline and serve from a
key-value store; the trie is the mental model, not the serving structure.

## Today's build (`w1d4_trie.py`)

- `Trie.insert(word, count=1)` accumulates counts, `contains(word)`, `starts_with(prefix) -> bool`,
  `delete(word)` (prunes nodes that become useless, returns False if absent),
  `top_k(prefix, k)` → list of words, sorted by (count desc, word asc).
- `node_count()` for tests (to check pruning).

## Staff angle

Asked "design typeahead", a staff candidate gets to the real constraints quickly: p99 < 50 ms
end to end means the suggestion lookup must be ~1–5 ms. So precompute per-prefix top-k, shard by
prefix, update offline daily plus a small real-time "trending" layer, filter for safety and
personalization at serve time. The trie answers "how do I store it", not "how do I serve it at 100k QPS".
