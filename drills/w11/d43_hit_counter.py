"""d43 Hit counter: hit(ts) records a hit at second ts (non-decreasing); get_hits(ts) returns hits in (ts - 300, ts].
O(1) memory in the number of hits per second: use 300 buckets."""


class HitCounter:
    def __init__(self):
        # TODO
        raise NotImplementedError

    def hit(self, ts: int) -> None:
        # TODO
        raise NotImplementedError

    def get_hits(self, ts: int) -> int:
        # TODO
        raise NotImplementedError
