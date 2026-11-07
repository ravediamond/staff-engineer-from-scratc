# Predict

1. Events for doc A: upsert v1, delete v3, upsert v2 (arrives late). With "last event wins", what is in the index?
   Guess:

2. Same with version checks but deletes implemented as removal (no tombstone)?
   Guess:

3. Same with version checks and versioned tombstones?
   Guess:

## Misses
-
