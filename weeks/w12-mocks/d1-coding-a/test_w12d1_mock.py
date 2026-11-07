import random
from collections import Counter

from w12d1_mock import TimeMap, least_interval


def test_timemap():
    t = TimeMap()
    t.set("model", "v1", 10)
    t.set("model", "v2", 20)
    assert t.get("model", 5) == ""
    assert t.get("model", 10) == "v1"
    assert t.get("model", 15) == "v1"
    assert t.get("model", 20) == "v2"
    assert t.get("model", 99) == "v2"
    assert t.get("other", 99) == ""


def simulate(tasks, n):
    """Brute-force greedy simulation: each tick run the available task with the most remaining."""
    remaining = Counter(tasks)
    ready_at = {k: 0 for k in remaining}
    t = 0
    while sum(remaining.values()):
        avail = [k for k in remaining if remaining[k] and ready_at[k] <= t]
        if avail:
            k = max(avail, key=lambda x: (remaining[x], x))
            remaining[k] -= 1
            ready_at[k] = t + n + 1
        t += 1
    return t


def test_least_interval():
    assert least_interval("AAABBB", 2) == 8
    assert least_interval("AAABBBCCCDDD", 2) == 12
    assert least_interval("AAABBB", 0) == 6
    assert least_interval("", 3) == 0
    rng = random.Random(0)
    for _ in range(200):
        tasks = "".join(rng.choice("ABCDE") for _ in range(rng.randint(1, 20)))
        n = rng.randint(0, 4)
        assert least_interval(tasks, n) == simulate(tasks, n), (tasks, n)
