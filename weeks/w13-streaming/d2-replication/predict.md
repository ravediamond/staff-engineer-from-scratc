# Predict

1. 3 replicas, all in the ISR. Leader LEO = 10, followers at 10 and 7. HW?
   Guess:

2. The follower at 7 is removed from the ISR (too slow). HW now?
   Guess:

3. `acks=1`: the leader writes offset 10, acknowledges, and dies before any follower fetched it. What does the producer believe, and what is true?
   Guess:

4. RF=3, min.insync.replicas=2, acks=all. How many brokers can fail with no loss of acknowledged data? And before writes are refused?
   Guess:

5. RF=3, min.insync.replicas=3. What happens during a rolling restart of the brokers?
   Guess:

## Misses
-
