"""Review: a candidate's TimeMap.get. It passed the three examples they wrote. As the interviewer, find the bug,
fix it, and write the feedback you would give in one line:

WHY:
"""
import bisect


class TimeMap:
    def __init__(self):
        self.data = {}

    def set(self, key, value, ts):
        self.data.setdefault(key, []).append((ts, value))

    def get(self, key, ts):
        pairs = self.data.get(key, [])
        stamps = [t for t, _ in pairs]
        i = bisect.bisect_right(stamps, ts)
        return pairs[i - 1][1] if i else ""
