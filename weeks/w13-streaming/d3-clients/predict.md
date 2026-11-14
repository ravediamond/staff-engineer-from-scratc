# Predict

1. A topic goes from 6 to 8 partitions. What fraction of keys now map to a different partition?
   Guess:

2. Idempotent producer: the broker last accepted seq 7 from this producer. It now receives seq 7 again, then seq 9. What does it do with each?
   Guess:

3. 7 partitions, 3 consumers, range assignment. How many partitions does each get?
   Guess:

4. 4 partitions, 6 consumers in one group. How many consumers do work?
   Guess:

5. A consumer's handler takes 10 minutes per batch; `max.poll.interval.ms` is 5 minutes. What happens, in a loop?
   Guess:

## Misses
-
