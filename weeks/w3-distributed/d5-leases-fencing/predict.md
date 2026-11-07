# Predict

1. Lease 10 s. Client renews every 3 s. A 15 s GC pause starts right after a renew. Who holds the lock when the client wakes up?
   Guess:

2. Redlock (5 Redis nodes, majority) without fencing tokens: safe against GC pauses?
   Guess:

3. The storage checks `token >= max_token`. Why `>=` and not `>`?
   Guess:

## Misses
-
