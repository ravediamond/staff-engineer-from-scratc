# Predict

1. Async replication, replica lag 2 s. A user saves their profile and the page reloads from a replica 200 ms later. What do they see?
   Guess:

2. Two replicas at LSN 90 and 100; the session's last write was LSN 95. Which replica may serve its read?
   Guess:

3. The primary acknowledged writes up to LSN 120; the best replica is at 112 when the primary dies. After failover, how many acknowledged writes are lost?
   Guess:

4. Same with synchronous replication to that replica?
   Guess:

5. The old primary comes back and still thinks it is primary. What is this called and what prevents it?
   Guess:

## Misses
-
