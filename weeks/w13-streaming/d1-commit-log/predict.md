# Predict

1. Segments of 4 records, 10 records appended. How many segments, and which offsets are in the active one?
   Guess:

2. Retention removes segments older than 7 days. The active segment's records are all 30 days old (a quiet topic). Is it deleted?
   Guess:

3. Log: (k1,a)@0 (k2,b)@1 (k1,c)@2 (k2,None)@3 (k3,d)@4, all in closed segments. After compaction, which offsets remain?
   Guess:

4. A consumer committed offset 2 before that compaction. What does it read next?
   Guess:

5. 1 GB segment, index entry every 4 KB. Roughly how many index entries, and how many bytes does a read scan after the index lookup?
   Guess:

## Misses
-
