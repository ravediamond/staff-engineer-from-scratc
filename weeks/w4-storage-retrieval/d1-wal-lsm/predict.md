# Predict

1. 1M random-key writes of 100 bytes. B-tree with 4 KB pages vs LSM: which writes more bytes to disk on ingest?
   Guess:

2. LSM with 10 SSTables, no bloom filters. A get for a key that does not exist reads how many files?
   Guess:

3. Crash during `append`: the WAL ends with `{"op": "put", "k": "a", "v`. What should replay do with it, and why only for the last line?
   Guess:

## Misses
-
