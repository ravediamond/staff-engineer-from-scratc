import pytest

from w13d3_clients import (GroupCoordinator, IdempotentBroker, OutOfOrderSequence, StaleGeneration, moved_fraction,
                           partition_for, range_assign)


def test_partitioner_is_stable_and_spreads():
    assert partition_for("order-42", 6) == partition_for("order-42", 6)
    assert partition_for("order-42", 6) == 4 and partition_for("été", 6) == 0
    counts = [0] * 6
    for i in range(6000):
        counts[partition_for(f"user-{i}", 6)] += 1
    assert min(counts) > 850 and max(counts) < 1150


def test_adding_partitions_moves_most_keys():
    keys = [f"user-{i}" for i in range(20000)]
    assert moved_fraction(keys, 6, 6) == 0
    assert abs(moved_fraction(keys, 6, 8) - 0.75) < 0.02
    assert abs(moved_fraction(keys, 6, 12) - 0.5) < 0.02


def test_idempotent_producer():
    b = IdempotentBroker()
    assert b.append(1, 0, "a") == ("ok", 0)
    assert b.append(1, 1, "b") == ("ok", 1)
    assert b.append(1, 1, "b") == ("duplicate", 1), "a retry is acknowledged with the original offset"
    assert b.append(2, 0, "c") == ("ok", 2), "sequences are per producer"
    assert b.log == ["a", "b", "c"]
    with pytest.raises(OutOfOrderSequence):
        b.append(1, 3, "gap")
    with pytest.raises(OutOfOrderSequence):
        b.append(1, 0, "too old")
    with pytest.raises(OutOfOrderSequence):
        b.append(9, 1, "new producer must start at 0")
    assert b.log == ["a", "b", "c"]


def test_range_assign():
    assert range_assign(["c2", "c1", "c3"], 7) == {"c1": [0, 1, 2], "c2": [3, 4], "c3": [5, 6]}
    a = range_assign([f"c{i}" for i in range(6)], 4)
    assert sorted(p for ps in a.values() for p in ps) == [0, 1, 2, 3]
    assert sum(1 for ps in a.values() if ps) == 4, "more consumers than partitions: the extra ones idle"


def test_group_rebalance_and_fencing():
    g = GroupCoordinator(4)
    gen1 = g.join("a")
    assert g.assignment == {"a": [0, 1, 2, 3]}
    g.commit("a", gen1, 3, 10)
    gen2 = g.join("b")
    assert gen2 == gen1 + 1 and g.assignment == {"a": [0, 1], "b": [2, 3]}
    with pytest.raises(StaleGeneration):
        g.commit("a", gen1, 3, 5)      # zombie: old generation
    with pytest.raises(StaleGeneration):
        g.commit("a", gen2, 3, 5)      # current generation but partition 3 now belongs to b
    g.commit("b", gen2, 3, 12)
    assert g.committed[3] == 12
    g.leave("a")
    assert g.assignment == {"b": [0, 1, 2, 3]} and g.generation == gen2 + 1


def test_lag():
    g = GroupCoordinator(3)
    gen = g.join("a")
    g.commit("a", gen, 0, 90)
    g.commit("a", gen, 1, 100)
    assert g.lag({0: 100, 1: 100, 2: 40}) == {0: 10, 1: 0, 2: 40}
