"""W1 D1: binary min-heap from scratch. No heapq, no sorted(). Write the invariant of each loop."""


class MinHeap:
    def __init__(self):
        self.a: list = []

    def __len__(self) -> int:
        return len(self.a)

    def peek(self):
        """Smallest item. IndexError if empty."""
        # TODO
        raise NotImplementedError

    def push(self, x) -> None:
        # TODO
        raise NotImplementedError

    def pop(self):
        """Remove and return the smallest item. IndexError if empty."""
        # TODO
        raise NotImplementedError

    def _sift_up(self, i: int) -> None:
        # TODO
        raise NotImplementedError

    def _sift_down(self, i: int) -> None:
        # TODO
        raise NotImplementedError


def _sift_down(a: list, i: int, n: int) -> None:
    """Repair the min-heap property below index i, considering only a[:n]."""
    # TODO
    raise NotImplementedError


def heapify(a: list) -> None:
    """In place, bottom-up, O(n): sift down every internal node from the last one to the root."""
    # TODO
    raise NotImplementedError


def heap_sort(a: list) -> list:
    """Return a NEW ascending list. Use heapify + repeated pops (or the in-place trick)."""
    # TODO
    raise NotImplementedError


def top_k_largest(stream, k: int) -> list:
    """k largest items of an iterable, sorted descending. O(n log k) time, O(k) memory."""
    # TODO
    raise NotImplementedError
