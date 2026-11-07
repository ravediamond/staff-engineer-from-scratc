# Predict

1. 1,000 calls of `await asyncio.sleep(1)` with `gather`, no semaphore. Wall time?
   Guess:

2. Same with `Semaphore(50)`. Wall time?
   Guess:

3. Producer makes 10,000 items instantly, consumer takes 1 ms each, queue `maxsize=0`. Peak queue size?
   Guess:

4. Target 50 req/s, model latency 4 s. How many concurrent requests do you need?
   Guess:

## Misses
-
