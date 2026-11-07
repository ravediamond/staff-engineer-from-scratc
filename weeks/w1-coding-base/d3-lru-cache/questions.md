# Questions

1. Why both a hash map and a doubly linked list? What does each give you, and why not a singly linked list?
2. Why sentinel nodes?
3. Lazy vs active expiry: trade-offs. What does Redis do?
4. Your cache hit rate drops from 92% to 40% every night at 2am, then recovers by 9am. Hypothesis, how you would confirm it, and two fixes.
5. Make this LRU safe for 64 threads. What is the simplest correct answer, and why might it not be good enough?

## Model answers

1. The map gives O(1) lookup of the node; the list gives O(1) reordering and O(1) access to the LRU end. Unlinking a node in O(1) requires its predecessor, which a singly linked list only gives after an O(n) walk.
2. With head and tail sentinels the list is never empty, so insert and unlink have no `if head is None` branches. Fewer branches, fewer bugs.
3. Lazy: zero background cost, but memory stays held by expired keys nobody reads. Active: frees memory, costs CPU, and is hard to make exact. Redis does both: lazy on access, plus about 10 times a second it samples 20 keys with a TTL, deletes the expired ones, and repeats while more than 25% were expired.
4. A nightly batch or scan job reading many cold keys once flushes the hot set (scan pollution). Confirm: hit rate per client or keyspace and job schedules around 2am, plus the fraction of reads hitting never-reread keys. Fixes: route the batch job around the cache (no cache-fill on reads from that client), a scan-resistant policy (2Q, ARC, TinyLFU admission), or a separate cache pool for batch.
5. One lock around get and put: correct, but every get is a write (it reorders the list), so all threads serialize. Better: shard the cache by key hash into N independent LRUs with their own locks, or approximate LRU with sampled eviction (Redis) or buffered access recording (Caffeine) to avoid writes on the read path.
