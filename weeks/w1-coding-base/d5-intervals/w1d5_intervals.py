"""W1 D5: intervals. Convention: half-open [start, end). Each interval is a pair (start, end) with start < end."""
import bisect


def merge(intervals: list) -> list:
    """Merge overlapping or touching intervals. Returns a sorted list of [start, end] lists."""
    out: list = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


def insert(intervals: list, new) -> list:
    """intervals: sorted, non-overlapping. Insert new and merge. O(n). Returns [start, end] lists."""
    ns, ne = new
    out, i, n = [], 0, len(intervals)
    while i < n and intervals[i][1] < ns:
        out.append(list(intervals[i]))
        i += 1
    while i < n and intervals[i][0] <= ne:
        ns, ne = min(ns, intervals[i][0]), max(ne, intervals[i][1])
        i += 1
    out.append([ns, ne])
    out.extend(list(x) for x in intervals[i:])
    return out


def max_concurrent(intervals: list) -> int:
    """Peak number of intervals active at the same time (half-open: touching ones do not overlap)."""
    events = []
    for s, e in intervals:
        events.append((s, 1))
        events.append((e, -1))
    events.sort()  # at equal time, -1 (end) sorts before +1 (start)
    cur = best = 0
    for _, d in events:
        cur += d
        best = max(best, cur)
    return best


class Calendar:
    """Accept a booking only if it overlaps no existing booking. O(log n) search."""

    def __init__(self):
        self.starts: list = []
        self.ends: list = []

    def book(self, start, end) -> bool:
        i = bisect.bisect_right(self.starts, start)
        if i > 0 and self.ends[i - 1] > start:
            return False
        if i < len(self.starts) and self.starts[i] < end:
            return False
        self.starts.insert(i, start)
        self.ends.insert(i, end)
        return True
