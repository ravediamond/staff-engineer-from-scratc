import random

import pytest

from w1d2_hashmap import OpenAddressingMap


class Collide:
    """Keys that all hash to the same slot: worst case for probing."""

    def __init__(self, v):
        self.v = v

    def __hash__(self):
        return 7

    def __eq__(self, o):
        return isinstance(o, Collide) and o.v == self.v


def test_put_get_overwrite_len():
    m = OpenAddressingMap()
    for i in range(100):
        m.put(f"k{i}", i)
    m.put("k5", 500)
    assert len(m) == 100
    assert m.get("k5") == 500
    assert m.get("k99") == 99
    assert "k42" in m and "nope" not in m
    with pytest.raises(KeyError):
        m.get("nope")


def test_delete_keeps_probe_chain():
    m = OpenAddressingMap(16)
    ks = [Collide(i) for i in range(6)]
    for i, k in enumerate(ks):
        m.put(k, i)
    m.delete(ks[1])
    m.delete(ks[3])
    assert m.get(ks[5]) == 5, "a key stored after a deleted one must still be found"
    assert ks[1] not in m
    with pytest.raises(KeyError):
        m.delete(ks[1])
    m.put(ks[1], 11)
    assert m.get(ks[1]) == 11 and len(m) == 5


def test_resize_and_load_factor():
    m = OpenAddressingMap(4)
    for i in range(1000):
        m.put(i, i * i)
    assert len(m) == 1000
    assert m.cap >= 1500, "should resize when load factor exceeds 2/3"
    assert all(m.get(i) == i * i for i in range(1000))


def test_tombstones_count_toward_resize():
    m = OpenAddressingMap(8)
    for round_ in range(200):
        m.put(("x", round_), round_)
        m.delete(("x", round_))
    m.probes = 0
    assert ("x", -1) not in m
    assert m.probes < 20, f"{m.probes} probes for one miss: tombstones never cleaned up"


def test_against_dict():
    rng = random.Random(0)
    m, ref = OpenAddressingMap(), {}
    for _ in range(3000):
        k = rng.randint(0, 200)
        op = rng.random()
        if op < 0.6:
            m.put(k, op)
            ref[k] = op
        elif k in ref:
            m.delete(k)
            del ref[k]
    assert len(m) == len(ref)
    assert sorted(m.keys()) == sorted(ref)
    assert all(m.get(k) == v for k, v in ref.items())
