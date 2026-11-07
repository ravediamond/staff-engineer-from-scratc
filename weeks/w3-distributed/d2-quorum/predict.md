# Predict

1. N=3, W=2, R=1. A write reaches replicas {0,1}. A read asks only replica 2. What does it see?
   Guess:

2. N=5, R=3, W=3. How many replica failures can you tolerate for writes? For reads?
   Guess:

3. N=3, R=2, W=2. Two clients write the same key concurrently with LWW timestamps from skewed clocks (client B is 5 s behind). B writes after A in real time. Which value survives?
   Guess:

## Misses
-
