"""Self-contained. Run after predict.md."""
from math import gcd

n_old, n_new = 6, 8
lcm = n_old * n_new // gcd(n_old, n_new)
same = sum(1 for h in range(lcm) if h % n_old == h % n_new) / lcm
print(f"1. {1 - same:.0%} of keys move (only hashes with h % 6 == h % 8 stay). Per-key order breaks across the change.")
print("2. seq 7: duplicate, dropped, acknowledged again. seq 9: OutOfOrderSequence (8 is missing), rejected.")
print("3. 3, 2, 2: the first (7 % 3) members get one extra.")
print("4. 4. Two consumers sit idle: parallelism is capped by the partition count.")
print("5. Kicked from the group -> rebalance -> the batch is redelivered to another member -> which also times out. "
      "A rebalance storm with zero progress. Fix: smaller batches, pause/resume with a worker pool, or a share group.")
