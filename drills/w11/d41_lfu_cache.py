"""d41 LFU cache with O(1) get/put. Evict the least frequently used; ties -> least recently used among them.
get returns -1 if missing. Capacity 0 stores nothing."""
from collections import OrderedDict, defaultdict


class LFUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.vals = {}
        self.freq = {}
        self.buckets = defaultdict(OrderedDict)  # freq -> keys in LRU order
        self.minf = 0

    def _touch(self, key):
        f = self.freq[key]
        del self.buckets[f][key]
        if not self.buckets[f]:
            del self.buckets[f]
            if self.minf == f:
                self.minf += 1
        self.freq[key] = f + 1
        self.buckets[f + 1][key] = None

    def get(self, key) -> int:
        if key not in self.vals:
            return -1
        self._touch(key)
        return self.vals[key]

    def put(self, key, value) -> None:
        if self.cap == 0:
            return
        if key in self.vals:
            self.vals[key] = value
            self._touch(key)
            return
        if len(self.vals) == self.cap:
            old, _ = self.buckets[self.minf].popitem(last=False)
            if not self.buckets[self.minf]:
                del self.buckets[self.minf]
            del self.vals[old]
            del self.freq[old]
        self.vals[key] = value
        self.freq[key] = 1
        self.buckets[1][key] = None
        self.minf = 1
