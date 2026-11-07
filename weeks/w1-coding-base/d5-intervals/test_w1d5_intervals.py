import random

from w1d5_intervals import Calendar, insert, max_concurrent, merge


def test_merge():
    assert merge([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    assert merge([[5, 7], [1, 2], [2, 4]]) == [[1, 4], [5, 7]]
    assert merge([[1, 10], [2, 3], [4, 5]]) == [[1, 10]]
    assert merge([]) == []


def test_insert():
    assert insert([[1, 3], [6, 9]], (2, 5)) == [[1, 5], [6, 9]]
    assert insert([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], (4, 8)) == [[1, 2], [3, 10], [12, 16]]
    assert insert([], (1, 2)) == [[1, 2]]
    assert insert([[3, 4]], (1, 2)) == [[1, 2], [3, 4]]
    assert insert([[1, 2]], (5, 6)) == [[1, 2], [5, 6]]


def test_insert_matches_merge():
    rng = random.Random(0)
    for _ in range(200):
        base = merge([(a, a + rng.randint(1, 5)) for a in (rng.randint(0, 50) for _ in range(8))])
        s = rng.randint(0, 55)
        new = (s, s + rng.randint(1, 8))
        assert insert(base, new) == merge(base + [list(new)])


def test_max_concurrent_half_open():
    assert max_concurrent([(1, 3), (3, 5), (2, 4)]) == 2
    assert max_concurrent([(0, 10), (1, 2), (2, 3), (3, 4)]) == 2
    assert max_concurrent([(0, 1)] * 5) == 5
    assert max_concurrent([]) == 0


def test_calendar():
    c = Calendar()
    assert c.book(10, 20)
    assert not c.book(15, 25)
    assert c.book(20, 30), "half-open: [10,20) and [20,30) do not overlap"
    assert not c.book(5, 11)
    assert c.book(5, 10)
    assert not c.book(0, 100)
    assert c.book(30, 31)


def test_calendar_random_vs_bruteforce():
    rng = random.Random(1)
    c, booked = Calendar(), []
    for _ in range(500):
        s = rng.randint(0, 1000)
        e = s + rng.randint(1, 30)
        ok = all(e <= bs or s >= be for bs, be in booked)
        assert c.book(s, e) == ok
        if ok:
            booked.append((s, e))
