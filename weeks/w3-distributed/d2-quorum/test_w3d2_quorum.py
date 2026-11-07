import pytest

from w3d2_quorum import Cluster, QuorumError, overlaps


def test_overlaps():
    assert overlaps(3, 2, 2) and overlaps(3, 1, 3)
    assert not overlaps(3, 1, 1) and not overlaps(5, 2, 3)


def test_quorum_read_sees_latest_write():
    c = Cluster(3, 2, 2)
    c.put("x", "v1", 1)
    c.put("x", "v2", 2, targets=[0, 1])
    for sources in ([0, 1], [0, 2], [1, 2]):
        assert c.get("x", sources=sources) == "v2", "any 2 of 3 overlap the write quorum"


def test_weak_quorum_can_be_stale():
    c = Cluster(3, 1, 1)
    c.put("x", "old", 1)
    c.put("x", "new", 2, targets=[0])
    assert c.get("x", sources=[2]) == "old"


def test_write_fails_without_quorum_but_partial_write_persists():
    c = Cluster(3, 2, 2)
    c.down = {1, 2}
    with pytest.raises(QuorumError):
        c.put("x", "v", 1)
    c.down = set()
    assert c.data[0]["x"] == (1, "v")


def test_read_needs_quorum():
    c = Cluster(3, 2, 2)
    c.put("x", "v", 1)
    c.down = {0, 1}
    with pytest.raises(QuorumError):
        c.get("x")


def test_read_repair():
    c = Cluster(3, 2, 2)
    c.put("x", "v1", 1)
    c.put("x", "v2", 2, targets=[0, 1])
    assert c.get("x", sources=[1, 2]) == "v2"
    assert c.data[2]["x"] == (2, "v2") and c.repairs == 1
    assert c.get("x", sources=[1, 2]) == "v2" and c.repairs == 1


def test_older_version_never_overwrites():
    c = Cluster(3, 2, 2)
    c.put("x", "new", 5)
    c.put("x", "late-old", 3)
    assert c.get("x") == "new"
    assert c.get("missing") is None
