# Predict

1. Dependency is down for 60 s. Client sends 100 req/s with 2 s timeout, no breaker. How many requests block for the full 2 s during the outage?
   Guess:

2. Same with a breaker (threshold 5, reset_timeout 5 s, half_open_max 1). Roughly how many requests reach the dead dependency during the 60 s?
   Guess:

3. Half-open with half_open_max = unlimited, dependency recovering and fragile, 100 req/s. What happens at the moment the timer expires?
   Guess:

## Misses
-
