"""d43 Hit counter: hit(ts) records a hit at second ts (non-decreasing); get_hits(ts) returns hits in (ts - 300, ts].
O(1) memory in the number of hits per second: use 300 buckets."""


class HitCounter:
    def __init__(self):
        self.times = [0] * 300
        self.counts = [0] * 300

    def hit(self, ts: int) -> None:
        i = ts % 300
        if self.times[i] != ts:
            self.times[i] = ts
            self.counts[i] = 0
        self.counts[i] += 1

    def get_hits(self, ts: int) -> int:
        return sum(c for t, c in zip(self.times, self.counts) if ts - t < 300)
