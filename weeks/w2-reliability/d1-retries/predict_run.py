"""Self-contained simulation. Run after predict.md."""
import random
from collections import Counter

random.seed(0)
print("1. no jitter, attempt index 7:", min(10, 0.1 * 2 ** 7), "s")


def peak(jitter):
    hits = Counter()
    for _ in range(1000):
        t = 0.0
        for attempt in range(6):
            d = min(10, 0.1 * 2 ** attempt)
            t += random.uniform(0, d) if jitter else d
            hits[int(t * 10)] += 1  # 100 ms buckets
    return max(hits.values())


print("2. no jitter, peak requests in one 100 ms window:", peak(False))
print("3. full jitter, peak requests in one 100 ms window:", peak(True))
print("4. 5 layers x 4 attempts each:", 4 ** 5, "backend requests per user request")
