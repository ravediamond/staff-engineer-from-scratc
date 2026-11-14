# Predict

1. T1 begins (snapshot isolation) and reads x = 10. T2 writes x = 20 and commits. T1 reads x again. Value?
   Guess:

2. Same under read committed. Value?
   Guess:

3. Snapshot isolation: T1 and T2 both read x = 10, both write x = 11. T1 commits. What happens to T2?
   Guess:

4. Read committed, same read-modify-write, done as `SELECT` then `UPDATE x = 11` in application code. Final x?
   Guess:

5. Two doctors on call, snapshot isolation, each transaction removes its own doctor after checking that the other is on call. Both commit?
   Guess:

6. A reporting transaction stays open for 6 hours on a table with heavy updates. What grows?
   Guess:

## Misses
-
