"""Review: an LRU someone wrote with OrderedDict. Tests in prod showed a hit rate that made no sense.
Find the bug, fix it, explain:

WHY:
"""
from collections import OrderedDict


class LRU:
    def __init__(self, cap):
        self.cap = cap
        self.d = OrderedDict()

    def get(self, k):
        if k not in self.d:
            return None
        self.d.move_to_end(k)
        return self.d[k]

    def put(self, k, v):
        self.d[k] = v
        self.d.move_to_end(k)
        if len(self.d) > self.cap:
            self.d.popitem(last=False)
