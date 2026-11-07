# Questions

1. Why does `hash % N` fail when N changes, and what fraction moves?
2. What do virtual nodes fix, and what do they cost?
3. Consistent hashing vs rendezvous hashing: when each?
4. One key gets 30% of all traffic. Consistent hashing does not help. What do you do?
5. Route LLM requests across 32 inference replicas to maximize prefix-cache hits without overloading any replica. Design the router.

## Model answers

1. A key stays put only if `h % N == h % (N+1)`, which holds for about 1/(N+1) of keys, so ~N/(N+1) of keys move (91% for 10→11). Every cache goes cold at once and every shard rebalances.
2. Uneven arcs and the single-successor dump: with V points per node the load spreads to about ±1/√V, and a leaving node's keys scatter across many nodes. Cost: V× more points (memory, membership metadata), slightly slower lookup, and more ranges to track during rebalancing.
3. Ring: O(log(NV)) lookup, used when N is large or ranges matter (Dynamo, Cassandra token ranges). Rendezvous: simpler, perfect balance and minimal movement, O(N) per lookup, natural for picking the top-k replicas (take the k highest weights). Good for small N.
4. Detect hot keys (sampling, top-k sketch). Reads: replicate the key to k nodes and spread reads, or put a near-cache in front. Writes: split the key (`key#0..k-1`, aggregate on read) if the semantics allow (counters, append-only), or coalesce requests. Long term: revisit the data model.
5. Hash the first ~N tokens (system prompt + early context, block-aligned) with consistent or rendezvous hashing to pick a preferred replica, giving cache affinity. Bound load: if the preferred replica's queue exceeds a threshold, fall back to the next replica on the ring ("consistent hashing with bounded loads", Mirrokni et al.). Track hit rate and per-replica queue depth. This is what prefix-aware routers in vLLM / SGLang deployments do.
