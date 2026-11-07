"""Self-contained: OrderedDict LRU simulator. Run after predict.md."""
import random
from collections import OrderedDict

random.seed(0)


def sim(cap, stream):
    c, hits = OrderedDict(), 0
    for k in stream:
        if k in c:
            hits += 1
            c.move_to_end(k)
        else:
            c[k] = 1
            if len(c) > cap:
                c.popitem(last=False)
    return hits / len(stream)


c = OrderedDict()
for op, k in [("put", "a"), ("put", "b"), ("get", "a"), ("put", "c")]:
    if op == "get":
        c.move_to_end(k)
    else:
        c[k] = 1
        if len(c) > 2:
            print("1. evicted:", c.popitem(last=False)[0])

N = 100_000
weights = [1 / (i + 1) for i in range(N)]
zipf = random.choices(range(N), weights=weights, k=200_000)
print(f"2. Zipf, cap=1% of keys: hit rate {sim(N // 100, zipf):.1%}")
scan = []
for i, z in enumerate(zipf):
    scan.append(z)
    scan.append(N + (i % N))
print(f"3. half the traffic is a looping scan: hit rate {sim(N // 100, scan):.1%} (scan items never hit and evict hot ones)")
print("4. lru_cache on a method keys on `self`: every instance stays referenced by the cache until evicted -> memory leak.")
print("   Fix: cache on a module-level function of the real inputs, or functools.cached_property, or weakref-based caches.")
