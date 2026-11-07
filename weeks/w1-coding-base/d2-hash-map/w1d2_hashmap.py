"""W1 D2: open-addressing hash map with linear probing and tombstones."""

_EMPTY = object()
_TOMB = object()


class OpenAddressingMap:
    def __init__(self, capacity: int = 8):
        self.cap = capacity
        self.keys_ = [_EMPTY] * capacity
        self.vals = [None] * capacity
        self.live = 0
        self.tombs = 0
        self.probes = 0  # total slots inspected, for tests

    def _find(self, key):
        """Return (index_of_key or None, first_free_index_for_insert).

        Walk from hash(key) % cap. Stop at an EMPTY slot. Remember the first tombstone
        seen: an insert may reuse it, but the search must continue past it.
        """
        i = hash(key) % self.cap
        first_free = None
        for _ in range(self.cap):
            self.probes += 1
            k = self.keys_[i]
            if k is _EMPTY:
                return None, (first_free if first_free is not None else i)
            if k is _TOMB:
                if first_free is None:
                    first_free = i
            elif k == key:
                return i, i
            i = (i + 1) % self.cap
        return None, first_free

    def _resize(self, new_cap: int) -> None:
        old = [(k, v) for k, v in zip(self.keys_, self.vals) if k is not _EMPTY and k is not _TOMB]
        self.cap = new_cap
        self.keys_ = [_EMPTY] * new_cap
        self.vals = [None] * new_cap
        self.live = self.tombs = 0
        for k, v in old:
            self.put(k, v)

    def put(self, key, value) -> None:
        idx, free = self._find(key)
        if idx is not None:
            self.vals[idx] = value
            return
        if self.keys_[free] is _TOMB:
            self.tombs -= 1
        self.keys_[free] = key
        self.vals[free] = value
        self.live += 1
        if (self.live + self.tombs) * 3 > self.cap * 2:
            self._resize(self.cap * 2)

    def get(self, key):
        idx, _ = self._find(key)
        if idx is None:
            raise KeyError(key)
        return self.vals[idx]

    def delete(self, key) -> None:
        idx, _ = self._find(key)
        if idx is None:
            raise KeyError(key)
        self.keys_[idx] = _TOMB
        self.vals[idx] = None
        self.live -= 1
        self.tombs += 1

    def __len__(self) -> int:
        return self.live

    def __contains__(self, key) -> bool:
        return self._find(key)[0] is not None

    def keys(self) -> list:
        return [k for k in self.keys_ if k is not _EMPTY and k is not _TOMB]
