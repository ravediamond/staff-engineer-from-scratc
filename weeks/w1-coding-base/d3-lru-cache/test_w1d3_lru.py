import random
from collections import OrderedDict

from w1d3_lru import LRUCache, TTLCache


def test_basic_eviction_order():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a") == 1
    c.put("c", 3)
    assert c.get("b") is None, "b was least recently used"
    assert c.keys_mru() == ["c", "a"]


def test_update_refreshes_recency():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("a", 10)
    c.put("c", 3)
    assert c.get("a") == 10 and c.get("b") is None
    assert len(c) == 2


def test_against_ordereddict():
    rng = random.Random(0)
    c, ref = LRUCache(5), OrderedDict()
    for _ in range(5000):
        k = rng.randint(0, 12)
        if rng.random() < 0.5:
            c.put(k, k * 2)
            ref[k] = k * 2
            ref.move_to_end(k)
            if len(ref) > 5:
                ref.popitem(last=False)
        else:
            expected = ref.get(k)
            if k in ref:
                ref.move_to_end(k)
            assert c.get(k) == expected
        assert c.keys_mru() == list(reversed(ref))


def test_no_ordereddict_used():
    import w1d3_lru

    assert "OrderedDict" not in open(w1d3_lru.__file__).read(), "write the linked list yourself"


def test_ttl_lazy_expiry():
    now = [0.0]
    c = TTLCache(10, ttl=5, clock=lambda: now[0])
    c.put("a", 1)
    now[0] = 4.9
    assert c.get("a") == 1
    now[0] = 5.0
    assert c.get("a") is None
    assert len(c) == 0


def test_ttl_purge_and_reput():
    now = [0.0]
    c = TTLCache(10, ttl=2, clock=lambda: now[0])
    for k in "abc":
        c.put(k, k)
    now[0] = 1
    c.put("a", "A")  # re-put refreshes expiry
    now[0] = 2.5
    assert c.purge_expired() == 2
    assert c.keys_mru() == ["a"] and c.get("a") == "A"
