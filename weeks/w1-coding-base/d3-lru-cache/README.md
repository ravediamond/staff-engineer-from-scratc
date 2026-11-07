# W1 D3: LRU and TTL caches in O(1)

Primer: `knowledge/01-python-for-interviews.md` §4. Production context: W4 D5 (cache-aside, stampedes).

## The one idea

LRU needs two things in O(1): **find by key** (hash map) and **reorder by recency** (doubly linked
list). The map points to list nodes; the list keeps most-recent at the head, least-recent at the tail.

```
map:  key -> node
list: HEAD <-> n3 <-> n1 <-> n7 <-> TAIL      (sentinels avoid every "if empty" branch)
get(k): node = map[k]; unlink(node); push_front(node)
put(k): if exists: update + move front; else: push_front; if size > cap: evict tail.prev
```

**Invariant:** `len(map) == number of real nodes in the list <= capacity`, and the list order is
exactly recency order. Every bug in an LRU breaks one of those two halves.

**TTL cache:** each entry also has `expires_at`. Two strategies: **lazy** (check on `get`, cheap,
memory held by dead entries) and **active** (a sweeper; Redis does lazy + sampled active
expiry). Today: lazy expiry plus a `purge_expired()` method, driven by an injected clock so tests
are deterministic. Never call `time.time()` directly in code you want to test.

## Today's build (`w1d3_lru.py`)

- `LRUCache(capacity)`: `get(key, default=None)`, `put(key, value)`, `__len__`, `keys_mru()` (most → least recent).
  Hand-written doubly linked list with sentinels. No `OrderedDict`.
- `TTLCache(capacity, ttl, clock)`: LRU + per-entry expiry, lazy on `get`, `purge_expired()` returns how many were removed.

## Staff angle

"LRU" in an interview is a data-structure question; in production it is a policy question. Scan
traffic (one big batch job reading everything once) flushes an LRU and destroys hit rate, which is
why databases use LRU-K, ARC, or 2Q, and why CDNs and Caffeine use TinyLFU admission. A staff
answer names the workload first: "What is the access distribution? Is there scan traffic? What
is a miss worth in latency and dollars?"
