"""W1 D1: binary min-heap from scratch. No heapq, no sorted(). Write the invariant of each loop."""


class MinHeap:
    def __init__(self):
        self.a: list = []

    def __len__(self) -> int:
        return len(self.a)

    def peek(self):
        """Smallest item. IndexError if empty."""
        if not self.a:
            raise IndexError("peek from empty heap")
        return self.a[0]

    def push(self, x) -> None:
        self.a.append(x)
        self._sift_up(len(self.a) - 1)

    def pop(self):
        """Remove and return the smallest item. IndexError if empty."""
        if not self.a:
            raise IndexError("pop from empty heap")
        last = self.a.pop()
        if not self.a:
            return last
        top, self.a[0] = self.a[0], last
        self._sift_down(0)
        return top

    def _sift_up(self, i: int) -> None:
        a = self.a
        # invariant: heap property holds everywhere except possibly between i and its parent
        while i > 0:
            p = (i - 1) // 2
            if a[i] < a[p]:
                a[i], a[p] = a[p], a[i]
                i = p
            else:
                break

    def _sift_down(self, i: int) -> None:
        _sift_down(self.a, i, len(self.a))


def _sift_down(a: list, i: int, n: int) -> None:
    """Repair the min-heap property below index i, considering only a[:n]."""
    # invariant: subtrees of i's children are heaps; only a[i] may be too big
    while True:
        l, r, smallest = 2 * i + 1, 2 * i + 2, i
        if l < n and a[l] < a[smallest]:
            smallest = l
        if r < n and a[r] < a[smallest]:
            smallest = r
        if smallest == i:
            return
        a[i], a[smallest] = a[smallest], a[i]
        i = smallest


def heapify(a: list) -> None:
    """In place, bottom-up, O(n): sift down every internal node from the last one to the root."""
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):
        _sift_down(a, i, n)


def heap_sort(a: list) -> list:
    """Return a NEW ascending list. Use heapify + repeated pops (or the in-place trick)."""
    h = list(a)
    heapify(h)
    out = []
    n = len(h)
    while n:
        out.append(h[0])
        n -= 1
        h[0] = h[n]
        _sift_down(h, 0, n)
    return out


def top_k_largest(stream, k: int) -> list:
    """k largest items of an iterable, sorted descending. O(n log k) time, O(k) memory."""
    if k <= 0:
        return []
    h = MinHeap()
    for x in stream:
        if len(h) < k:
            h.push(x)
        elif x > h.peek():
            h.a[0] = x
            h._sift_down(0)
    out = []
    while len(h):
        out.append(h.pop())
    return out[::-1]
