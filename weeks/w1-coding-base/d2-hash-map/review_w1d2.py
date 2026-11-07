"""Review: a linear-probing map someone 'simplified'. Find the bug, fix it, explain:

WHY:
"""

EMPTY = None


class TinyMap:
    def __init__(self, cap=16):
        self.slots = [EMPTY] * cap  # each slot: None, "TOMB", or (key, value)

    def _start(self, key):
        return hash(key) % len(self.slots)

    def put(self, key, value):
        i = self._start(key)
        while self.slots[i] is not EMPTY and self.slots[i] != "TOMB" and self.slots[i][0] != key:
            i = (i + 1) % len(self.slots)
        self.slots[i] = (key, value)

    def get(self, key):
        i = self._start(key)
        while self.slots[i] is not EMPTY:
            if self.slots[i] != "TOMB" and self.slots[i][0] == key:
                return self.slots[i][1]
            i = (i + 1) % len(self.slots)
        raise KeyError(key)

    def delete(self, key):
        i = self._start(key)
        while self.slots[i] is not EMPTY:
            if self.slots[i] != "TOMB" and self.slots[i][0] == key:
                self.slots[i] = EMPTY
                return
            i = (i + 1) % len(self.slots)
        raise KeyError(key)
