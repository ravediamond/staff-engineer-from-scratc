# Predict

1. Code: `db.commit(order)` then `kafka.send(event)`. The process is killed between the two. What do downstream systems believe?
   Guess:

2. Reverse the order: send, then commit. The commit fails. Now what?
   Guess:

3. The relay publishes an outbox row, crashes before marking it published. After restart?
   Guess:

4. Schema v2 adds field `currency` with no default. Is v2 BACKWARD compatible with v1? FORWARD?
   Guess:

5. Target 200 MB/s, a partition takes 10 MB/s, one consumer instance processes 5 MB/s, headroom 1.5×. Partitions?
   Guess:

## Misses
-
