"""W1 D5: intervals. Convention: half-open [start, end). Each interval is a pair (start, end) with start < end."""
import bisect


def merge(intervals: list) -> list:
    """Merge overlapping or touching intervals. Returns a sorted list of [start, end] lists."""
    # TODO
    raise NotImplementedError


def insert(intervals: list, new) -> list:
    """intervals: sorted, non-overlapping. Insert new and merge. O(n). Returns [start, end] lists."""
    # TODO
    raise NotImplementedError


def max_concurrent(intervals: list) -> int:
    """Peak number of intervals active at the same time (half-open: touching ones do not overlap)."""
    # TODO
    raise NotImplementedError


class Calendar:
    """Accept a booking only if it overlaps no existing booking. O(log n) search."""

    def __init__(self):
        self.starts: list = []
        self.ends: list = []

    def book(self, start, end) -> bool:
        # TODO
        raise NotImplementedError
