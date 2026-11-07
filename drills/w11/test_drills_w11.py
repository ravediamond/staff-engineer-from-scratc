from d41_lfu_cache import LFUCache
from d42_min_stack import MinStack
from d43_hit_counter import HitCounter
from d44_snapshot_array import SnapshotArray


def test_d41():
    c = LFUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)  # evicts 2 (freq 1)
    assert c.get(2) == -1 and c.get(3) == 3
    c.put(4, 4)  # 1 and 3 both freq 2: evict LRU = 1
    assert c.get(1) == -1 and c.get(3) == 3 and c.get(4) == 4
    z = LFUCache(0)
    z.put(1, 1)
    assert z.get(1) == -1


def test_d42():
    s = MinStack()
    for x in [-2, 0, -3]:
        s.push(x)
    assert s.get_min() == -3
    s.pop()
    assert s.top() == 0 and s.get_min() == -2


def test_d43():
    h = HitCounter()
    for t in [1, 2, 3, 3]:
        h.hit(t)
    assert h.get_hits(4) == 4
    h.hit(300)
    assert h.get_hits(300) == 5 and h.get_hits(301) == 4 and h.get_hits(603) == 0


def test_d44():
    a = SnapshotArray(3)
    a.set(0, 5)
    assert a.snap() == 0
    a.set(0, 6)
    a.set(0, 7)
    assert a.get(0, 0) == 5 and a.get(1, 0) == 0
    assert a.snap() == 1 and a.get(0, 1) == 7
