# Predict

1. base=0.1 s, cap=10 s, no jitter. Delay before attempt 8 (attempt index 7)?
   Guess:

2. 1,000 clients fail at t=0 and retry with exponential backoff, NO jitter. Peak requests per 100 ms window during retries: ~10, ~100, ~1,000?
   Guess:

3. Same with full jitter. Peak per 100 ms window?
   Guess:

4. Five layers, each retries 3 times (4 attempts) on failure, backend 100% down. Backend requests per user request?
   Guess:

## Misses
-
