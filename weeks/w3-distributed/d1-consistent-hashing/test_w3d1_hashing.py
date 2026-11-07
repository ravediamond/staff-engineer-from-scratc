from w3d1_hashing import Ring, max_over_mean, moved_fraction, rendezvous, stable_hash

KEYS = [f"k{i}" for i in range(20000)]


def test_stable_hash():
    assert stable_hash("abc") == stable_hash("abc")
    assert stable_hash("abc") != stable_hash("abd")
    assert 0 <= stable_hash("x") < 2 ** 64


def test_wraparound():
    r = Ring(vnodes=1)
    r.add("only")
    assert all(r.lookup(k) == "only" for k in KEYS[:500])


def test_add_moves_about_one_over_n_plus_one():
    r = Ring(vnodes=150)
    for i in range(10):
        r.add(f"n{i}")
    before = r.assignment(KEYS)
    r.add("n10")
    after = r.assignment(KEYS)
    f = moved_fraction(before, after)
    assert 0.06 < f < 0.13, f
    moved_to = {after[k] for k in KEYS if before[k] != after[k]}
    assert moved_to == {"n10"}, "keys only move TO the new node"


def test_remove_only_moves_its_keys():
    r = Ring(vnodes=150)
    for i in range(8):
        r.add(f"n{i}")
    before = r.assignment(KEYS)
    r.remove("n3")
    after = r.assignment(KEYS)
    assert all(after[k] == before[k] for k in KEYS if before[k] != "n3")
    assert "n3" not in set(after.values())


def test_vnodes_balance():
    one, many = Ring(vnodes=1), Ring(vnodes=200)
    for i in range(10):
        one.add(f"n{i}")
        many.add(f"n{i}")
    assert max_over_mean(many.assignment(KEYS)) < 1.25
    assert max_over_mean(one.assignment(KEYS)) > max_over_mean(many.assignment(KEYS))


def test_rendezvous_minimal_movement():
    nodes = [f"n{i}" for i in range(10)]
    a = {k: rendezvous(k, nodes) for k in KEYS[:5000]}
    b = {k: rendezvous(k, nodes + ["n10"]) for k in KEYS[:5000]}
    assert all(b[k] in (a[k], "n10") for k in a)
    assert 0.06 < moved_fraction(a, b) < 0.13
