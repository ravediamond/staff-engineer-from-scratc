"""W12 D1: coding mock A. Timer: 35 minutes for both."""
import bisect
from collections import Counter, defaultdict


class TimeMap:
    def __init__(self):
        self.ts: dict = defaultdict(list)
        self.vals: dict = defaultdict(list)

    def set(self, key: str, value: str, ts: int) -> None:
        # TODO
        raise NotImplementedError

    def get(self, key: str, ts: int) -> str:
        # TODO
        raise NotImplementedError


def least_interval(tasks: str, n: int) -> int:
    # TODO
    raise NotImplementedError
