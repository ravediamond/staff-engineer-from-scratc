from w3d4_raft import Follower, Leader, replicate_until_stable


def terms(log):
    return [t for t, _ in log]


def test_reject_stale_term_and_mismatch():
    f = Follower([(1, "a"), (1, "b"), (2, "c")], current_term=3)
    assert f.append_entries(2, 3, 2, [], 0) == (False, 0), "stale leader"
    assert f.append_entries(3, 3, 1, [(3, "x")], 0) == (False, 0), "prev term mismatch"
    assert f.append_entries(3, 5, 2, [(3, "x")], 0) == (False, 0), "follower too short"


def test_truncate_conflict_and_append():
    f = Follower([(1, "a"), (1, "b"), (2, "c"), (2, "d"), (2, "e")], current_term=2)
    ok, m = f.append_entries(3, 3, 2, [(3, "x")], 0)
    assert ok and m == 4
    assert terms(f.log) == [1, 1, 2, 3]


def test_duplicate_or_old_request_does_not_truncate():
    f = Follower([], current_term=1)
    assert f.append_entries(1, 0, 0, [(1, "a"), (1, "b"), (1, "c")], 0) == (True, 3)
    assert f.append_entries(1, 0, 0, [(1, "a")], 0) == (True, 1)
    assert len(f.log) == 3, "a delayed duplicate must not delete later entries"


def test_commit_index_bounded_by_new_entries():
    f = Follower([], current_term=1)
    f.append_entries(1, 0, 0, [(1, "a"), (1, "b")], leader_commit=10)
    assert f.commit_index == 2


def test_leader_catches_up_divergent_follower():
    leader = Leader([(1, "a"), (1, "b"), (3, "c"), (3, "d")], current_term=3, follower_ids=["f1", "f2"])
    f1 = Follower([(1, "a"), (1, "b"), (2, "x"), (2, "y"), (2, "z")], current_term=2)
    f2 = Follower([(1, "a")], current_term=1)
    replicate_until_stable(leader, {"f1": f1, "f2": f2})
    assert f1.log == leader.log and f2.log == leader.log
    assert leader.commit_index == 4


def test_figure8_rule():
    # Leader of term 4 holds an old term-2 entry at index 2, replicated to a majority, plus nothing new yet.
    leader = Leader([(1, "a"), (2, "old")], current_term=4, follower_ids=["f1", "f2", "f3", "f4"])
    nodes = {f: Follower([(1, "a")], current_term=2) for f in ["f1", "f2", "f3", "f4"]}
    replicate_until_stable(leader, nodes, reachable=["f1", "f2"])
    assert leader.match_index["f1"] == 2 and leader.match_index["f2"] == 2
    assert leader.commit_index == 0 or leader.commit_index == 1
    assert leader.commit_index < 2, "never commit an older-term entry by counting replicas"
    leader.append("new")
    replicate_until_stable(leader, nodes, reachable=["f1", "f2"])
    assert leader.commit_index == 3, "the current-term entry commits, and index 2 with it"
