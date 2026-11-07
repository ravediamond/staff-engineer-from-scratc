# Predict

1. LRU capacity 2. Ops: put(a), put(b), get(a), put(c). Which key was evicted?
   Guess:

2. Same cache, Zipf-distributed keys (a few very hot), capacity = 1% of distinct keys. Hit rate: ~1%, ~10%, ~50%+?
   Guess:

3. Same cache, but now 50% of traffic is a sequential scan over all keys, looping. Hit rate goes up, down, or to ~0?
   Guess:

4. `functools.lru_cache` on a method of a class with 1M short-lived instances. What leaks?
   Guess:

## Misses
-
