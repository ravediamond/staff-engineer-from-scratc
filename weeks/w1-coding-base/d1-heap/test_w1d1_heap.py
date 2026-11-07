import random

import pytest

from w1d1_heap import MinHeap, heap_sort, heapify, top_k_largest


def is_min_heap(a):
    return all(a[(i - 1) // 2] <= a[i] for i in range(1, len(a)))


def test_push_pop_sorted_order():
    rng = random.Random(1)
    xs = [rng.randint(-50, 50) for _ in range(300)]
    h = MinHeap()
    for x in xs:
        h.push(x)
        assert is_min_heap(h.a), "heap property broken after a push"
    out = [h.pop() for _ in range(len(xs))]
    assert out == sorted(xs)
    assert len(h) == 0


def test_peek_and_empty_errors():
    h = MinHeap()
    with pytest.raises(IndexError):
        h.pop()
    with pytest.raises(IndexError):
        h.peek()
    h.push(4)
    h.push(2)
    assert h.peek() == 2 and len(h) == 2


def test_heapify_in_place():
    rng = random.Random(2)
    for n in [0, 1, 2, 3, 10, 101]:
        a = [rng.random() for _ in range(n)]
        before = sorted(a)
        ret = heapify(a)
        assert ret is None, "heapify works in place and returns None"
        assert is_min_heap(a)
        assert sorted(a) == before


def test_heapify_is_linear():
    class C(int):
        n = 0

        def __lt__(self, o):
            C.n += 1
            return int.__lt__(self, o)

    a = [C(x) for x in range(20000, 0, -1)]  # worst order for a min-heap
    C.n = 0
    heapify(a)
    assert C.n < 4 * len(a), f"{C.n} comparisons for n={len(a)}: that is not O(n) bottom-up heapify"


def test_heap_sort():
    rng = random.Random(3)
    a = [rng.randint(0, 9) for _ in range(200)]
    copy = list(a)
    assert heap_sort(a) == sorted(copy)
    assert a == copy, "heap_sort must not modify its input"
    assert heap_sort([]) == []


def test_top_k():
    rng = random.Random(4)
    xs = [rng.random() for _ in range(5000)]
    assert top_k_largest(iter(xs), 7) == sorted(xs, reverse=True)[:7]
    assert top_k_largest([3, 1, 3, 2], 2) == [3, 3]
    assert top_k_largest([1, 2], 5) == [2, 1]
    assert top_k_largest([1, 2], 0) == []
