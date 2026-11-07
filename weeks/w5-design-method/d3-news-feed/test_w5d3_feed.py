from w5d3_feed import FeedService, fanout_writes


def build():
    f = FeedService(celebrity_threshold=3, inbox_cap=5)
    for fan in ["u1", "u2", "u3", "u4"]:
        f.follow(fan, "star")
    f.follow("u1", "bob")
    f.follow("u2", "bob")
    return f


def test_push_for_normal_pull_for_celebrity():
    f = build()
    f.post("bob", 1, ts=10)
    f.post("star", 2, ts=11)
    assert f.writes == 2, "bob has 2 followers; star is a celebrity: no fan-out"
    assert f.feed("u1", 10) == [2, 1]
    assert f.feed("u3", 10) == [2]
    assert f.feed("bob", 10) == [1], "own posts appear"


def test_order_cap_and_ties():
    f = build()
    for i in range(8):
        f.post("bob", 100 + i, ts=i)
    assert f.inbox["u1"] == [(7, 107), (6, 106), (5, 105), (4, 104), (3, 103)]
    f.post("star", 500, ts=5)
    assert f.feed("u1", 4) == [107, 106, 500, 105]


def test_reads_counted():
    f = build()
    f.reads = 0
    f.feed("u1", 3)
    assert f.reads == 3, "inbox + own outbox + 1 celebrity"


def test_fanout_writes():
    assert fanout_writes({"a": 10, "b": 200, "c": 5_000_000}, threshold=1_000_000) == 210
