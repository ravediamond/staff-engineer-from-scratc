import pytest

from w5d2_ids import (ClockMovedBackwards, Snowflake, base62_decode, base62_encode, decode_cursor, encode_cursor,
                      paginate, snowflake_decode)


def test_base62_roundtrip():
    for n in [0, 1, 61, 62, 3843, 3844, 10 ** 12, 62 ** 7 - 1]:
        assert base62_decode(base62_encode(n)) == n
    assert base62_encode(61) == "z" and base62_encode(62) == "10"
    assert len(base62_encode(62 ** 7 - 1)) == 7


def test_snowflake_layout_and_order():
    t = [1000]
    g = Snowflake(worker_id=5, clock_ms=lambda: t[0])
    a, b = g.next_id(), g.next_id()
    assert snowflake_decode(a) == (1000, 5, 0) and snowflake_decode(b) == (1000, 5, 1)
    t[0] = 1001
    c = g.next_id()
    assert snowflake_decode(c) == (1001, 5, 0) and a < b < c


def test_snowflake_sequence_overflow_waits():
    calls = {"n": 0}

    def clock():
        calls["n"] += 1
        return 7 if calls["n"] <= 4100 else 8

    g = Snowflake(worker_id=1, clock_ms=clock)
    ids = [g.next_id() for _ in range(4097)]
    assert len(set(ids)) == 4097
    assert snowflake_decode(ids[-1])[0] == 8 and snowflake_decode(ids[-1])[2] == 0


def test_snowflake_clock_backwards():
    t = [50]
    g = Snowflake(worker_id=1, clock_ms=lambda: t[0])
    g.next_id()
    t[0] = 49
    with pytest.raises(ClockMovedBackwards):
        g.next_id()


def test_cursor_opaque_roundtrip():
    c = encode_cursor(1700, 42)
    assert "1700" not in c and decode_cursor(c) == (1700, 42)


def test_paginate_walks_everything_once():
    items = [{"id": i, "created_at": i // 3} for i in range(25)]
    seen, cur = [], None
    while True:
        page, cur = paginate(items, 7, cur)
        seen += [x["id"] for x in page]
        if cur is None:
            break
    assert seen == sorted(range(25), key=lambda i: (i // 3, i), reverse=True)


def test_paginate_stable_under_inserts():
    items = [{"id": i, "created_at": i} for i in range(10)]
    p1, cur = paginate(items, 4)
    items += [{"id": 100 + j, "created_at": 50 + j} for j in range(3)]  # new items at the top
    p2, _ = paginate(items, 4, cur)
    assert [x["id"] for x in p1] == [9, 8, 7, 6]
    assert [x["id"] for x in p2] == [5, 4, 3, 2], "no duplicates from new inserts"
