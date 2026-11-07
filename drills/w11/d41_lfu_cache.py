"""d41 LFU cache with O(1) get/put. Evict the least frequently used; ties -> least recently used among them.
get returns -1 if missing. Capacity 0 stores nothing."""
from collections import OrderedDict, defaultdict


class LFUCache:
    def __init__(self, capacity: int):
        # TODO
        raise NotImplementedError

    def _touch(self, key):
        # TODO
        raise NotImplementedError

    def get(self, key) -> int:
        # TODO
        raise NotImplementedError

    def put(self, key, value) -> None:
        # TODO
        raise NotImplementedError
