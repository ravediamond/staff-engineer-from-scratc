# Predict

1. Backfill reads key k (version 3) from old; meanwhile a dual write puts version 4 into new; then backfill writes version 3 into new. What is in new?
   Guess:

2. Verification finds a 0.3% mismatch rate on 10M keys. Cut over?
   Guess:

3. Why keep writing to the old store after cutover?
   Guess:

## Misses
-
