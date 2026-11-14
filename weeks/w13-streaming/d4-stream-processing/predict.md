# Predict

1. Window 60 s, max_out_of_order 10 s, one partition. Events at event times 5, 50, 62, 58, 71. After which event does window [0, 60) fire?
   Guess:

2. Two partitions. Partition 0 has seen event time 500, partition 1 only 90. Bound 10 s. Watermark?
   Guess:

3. Allowed lateness 30 s. An event for window [0, 60) arrives when the watermark is 75. Counted? And at watermark 95?
   Guess:

4. The job crashes after processing offsets 0–99 and checkpointed at offset 59. After restore, which offsets are replayed, and why are counts not doubled?
   Guess:

5. 100 billion events/day. Events per second on average? At a 3× peak?
   Guess:

## Misses
-
