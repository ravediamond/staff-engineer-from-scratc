"""Self-contained. Run after predict.md."""
from collections import Counter


def least(tasks, n):
    c = Counter(tasks)
    m = max(c.values())
    k = sum(1 for v in c.values() if v == m)
    return max(len(tasks), (m - 1) * (n + 1) + k)


print("1.", least("AAABBB", 2), "(A B _ A B _ A B)")
print("2.", least("AAABBBCCCDDD", 2), "(no idle needed: the formula's max with len(tasks) matters)")
print("3. bisect.bisect_right on the per-key timestamp list, minus one")
