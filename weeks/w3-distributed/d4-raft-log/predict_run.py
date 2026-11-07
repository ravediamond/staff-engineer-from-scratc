"""Self-contained. Run after predict.md."""
print("1. 5 nodes: majority = 3 -> tolerates 2 failures")
log = [1, 1, 2, 2, 2]
print("2. log[4] term is", log[4 - 1], "!= 3 -> reject; leader decrements next_index and retries")
log = log[:3] + [3]
print("3. entry at index 4 has term 2, new entry term 3 -> conflict -> truncate from 4 and append:", log)
print("4. majority of 3 = leader + 1: wait for the nearest follower -> ~80 ms (one RTT to Virginia) + fsync")
