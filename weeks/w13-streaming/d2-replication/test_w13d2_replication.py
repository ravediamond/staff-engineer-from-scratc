import pytest

from w13d2_replication import NotEnoughReplicas, Partition, PartitionOffline


def test_hw_is_min_over_isr_and_gates_consumers():
    p = Partition()
    offs = [p.produce(v, "all") for v in "abc"]
    assert offs == [0, 1, 2] and p.hw == 0
    assert not p.acked(2, "all") and p.acked(2, 1) and p.fetch(0) == []
    p.replicate(1)
    assert p.hw == 0, "replica 2 is still in the ISR at LEO 0"
    p.replicate(2, max_records=2)
    assert p.hw == 2 and p.fetch(0) == ["a", "b"]
    assert p.acked(1, "all") and not p.acked(2, "all")


def test_acks_1_loses_data_on_leader_failure_acks_all_does_not():
    p = Partition()
    o = p.produce("committed", "all")
    p.replicate(1)
    p.replicate(2)
    assert p.acked(o, "all")
    lost = p.produce("only-on-leader", 1)
    assert p.acked(lost, 1)
    p.fail(0)
    assert p.leader == 1 and p.epoch == 1
    assert p.logs[p.leader] == ["committed"], "the acks=1 record is gone; the acks=all record survived"
    assert p.fetch(0) == ["committed"]


def test_shrinking_isr_unblocks_hw_then_min_insync_blocks_writes():
    p = Partition(min_insync=2)
    p.produce("a", "all")
    p.replicate(1)
    assert p.hw == 0
    p.shrink_isr(2)
    assert p.isr == {0, 1} and p.hw == 1
    p.shrink_isr(0)
    assert 0 in p.isr, "the leader never leaves the ISR"
    p.fail(1)
    with pytest.raises(NotEnoughReplicas):
        p.produce("b", "all")
    assert p.logs[0] == ["a"], "a refused write is not appended"
    assert p.produce("b", 1) == 1, "acks=1 still accepted: weaker promise"


def test_follower_rejoins_isr_only_when_caught_up():
    p = Partition()
    for v in "abcd":
        p.produce(v, 1)
    p.shrink_isr(2)
    p.replicate(2, max_records=2)
    assert 2 not in p.isr
    p.replicate(2)
    assert 2 in p.isr


def test_clean_election_goes_offline_rather_than_lose_data():
    p = Partition(unclean=False)
    p.produce("a", "all")
    p.shrink_isr(1)
    p.shrink_isr(2)
    assert p.hw == 1 and p.acked(0, "all"), "ISR = {leader}: committed on the leader alone (min.insync only gates new writes)"
    p.fail(0)
    assert p.leader is None
    with pytest.raises(PartitionOffline):
        p.produce("b", 1)
    with pytest.raises(PartitionOffline):
        p.fetch(0)


def test_unclean_election_loses_committed_data():
    p = Partition(unclean=True)
    p.produce("a", 1)
    p.shrink_isr(1)
    p.shrink_isr(2)
    assert p.hw == 1
    p.fail(0)
    assert p.leader == 1 and p.isr == {1}
    assert p.hw == 0 and p.fetch(0) == [], "a record that consumers could already read has vanished"


def test_old_leader_truncates_divergent_records():
    p = Partition()
    p.produce("a", "all")
    p.replicate(1)
    p.replicate(2)
    p.produce("zombie", 1)             # only on replica 0
    p.fail(0)
    p.produce("b", "all")              # new leader 1 writes offset 1
    p.recover(0)
    assert 0 not in p.isr
    p.replicate(0)
    assert p.logs[0] == ["a", "b"] and 0 in p.isr
    p.replicate(2)
    assert p.hw == 2
