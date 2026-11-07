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
        # TODO
        raise NotImplementedError

    def _resize(self, new_cap: int) -> None:
        # TODO
        raise NotImplementedError

    def put(self, key, value) -> None:
        # TODO
        raise NotImplementedError

    def get(self, key):
        # TODO
        raise NotImplementedError

    def delete(self, key) -> None:
        # TODO
        raise NotImplementedError

    def __len__(self) -> int:
        return self.live

    def __contains__(self, key) -> bool:
        # TODO
        raise NotImplementedError

    def keys(self) -> list:
        # TODO
        raise NotImplementedError
