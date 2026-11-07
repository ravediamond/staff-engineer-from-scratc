"""W12 D1: coding mock A. Timer: 35 minutes for both."""
import bisect
from collections import Counter, defaultdict


class TimeMap:
    def __init__(self):
        self.ts: dict = defaultdict(list)
        self.vals: dict = defaultdict(list)

    def set(self, key: str, value: str, ts: int) -> None:
        self.ts[key].append(ts)
        self.vals[key].append(value)

    def get(self, key: str, ts: int) -> str:
        i = bisect.bisect_right(self.ts.get(key, []), ts)
        return self.vals[key][i - 1] if i else ""


def least_interval(tasks: str, n: int) -> int:
    if not tasks:
        return 0
    c = Counter(tasks)
    m = max(c.values())
    k = sum(1 for v in c.values() if v == m)
    return max(len(tasks), (m - 1) * (n + 1) + k)
