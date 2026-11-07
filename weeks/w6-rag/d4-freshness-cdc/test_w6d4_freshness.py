import itertools
import random

from w6d4_freshness import VersionedIndex


def up(d, v, text):
    return {"op": "upsert", "doc_id": d, "version": v, "text": text}


def rm(d, v):
    return {"op": "delete", "doc_id": d, "version": v}


def test_upsert_replaces_chunks():
    idx = VersionedIndex(chunk_size=5)
    assert idx.apply(up("a", 1, "hello world"))
    assert idx.chunks_for("a") == ["a@1#0", "a@1#1", "a@1#2"]
    idx.apply(up("a", 2, "bye"))
    assert idx.chunks_for("a") == ["a@2#0"]
    assert idx.search("hello") == [] and idx.search("BYE") == ["a"]


def test_out_of_order_and_duplicates():
    idx = VersionedIndex()
    assert idx.apply(up("a", 2, "new text"))
    assert not idx.apply(up("a", 1, "old text"))
    assert not idx.apply(up("a", 2, "new text"))
    assert idx.search("old") == [] and idx.applied == 1


def test_tombstone_blocks_resurrection():
    idx = VersionedIndex()
    idx.apply(up("a", 1, "pump manual"))
    idx.apply(rm("a", 3))
    assert not idx.apply(up("a", 2, "pump manual v2 (late)"))
    assert idx.live_doc_ids() == [] and idx.search("pump") == []
    assert idx.apply(up("a", 4, "recreated"))
    assert idx.live_doc_ids() == ["a"]


def test_any_order_converges():
    events = [up("a", 1, "one"), up("a", 2, "two"), rm("a", 3), up("b", 1, "bee"), up("b", 5, "bee five"),
              rm("c", 2), up("c", 1, "cee")]
    for perm in random.Random(0).sample(list(itertools.permutations(events)), 200):
        idx = VersionedIndex()
        for e in perm + perm:  # delivered twice
            idx.apply(e)
        assert idx.live_doc_ids() == ["b"]
        assert idx.search("five") == ["b"] and idx.search("two") == []


def test_staleness():
    idx = VersionedIndex()
    idx.apply(up("a", 3, "x"))
    idx.apply(up("b", 1, "y"))
    assert idx.staleness({"a": 3, "b": 2, "c": 1}) == ["b", "c"]
