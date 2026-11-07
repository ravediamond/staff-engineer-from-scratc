from w3d3_clocks import LamportClock, siblings, vc_compare, vc_increment, vc_merge


def test_lamport_happens_before():
    a, b = LamportClock(), LamportClock()
    e1 = a.tick()
    m = a.send()
    e2 = b.tick()
    r = b.receive(m)
    assert e1 < m < r
    assert (e1, m, e2, r) == (1, 2, 1, 3)
    assert b.receive(1) == 4, "receive never goes backwards"


def test_vc_increment_and_merge_pure():
    a = {"x": 1}
    b = vc_increment(a, "y")
    assert a == {"x": 1} and b == {"x": 1, "y": 1}
    assert vc_merge({"x": 3, "y": 0}, {"x": 1, "y": 2, "z": 1}) == {"x": 3, "y": 2, "z": 1}


def test_vc_compare():
    assert vc_compare({"a": 1}, {"a": 1}) == "equal"
    assert vc_compare({}, {"a": 1}) == "before"
    assert vc_compare({"a": 1}, {"a": 1, "b": 1}) == "before"
    assert vc_compare({"a": 2, "b": 1}, {"a": 1, "b": 1}) == "after"
    assert vc_compare({"a": 2, "b": 1}, {"a": 1, "b": 2}) == "concurrent"
    assert vc_compare({"a": 1, "b": 0}, {"a": 1}) == "equal"


def test_message_flow():
    a, b = {}, {}
    a = vc_increment(a, "A")              # A writes
    b = vc_increment(vc_merge(b, a), "B")  # B receives and writes
    assert vc_compare(a, b) == "before"
    a2 = vc_increment(a, "A")             # A writes again without seeing B
    assert vc_compare(a2, b) == "concurrent"


def test_siblings():
    v1 = ({"r1": 1}, "a")
    v2 = ({"r1": 1, "r2": 1}, "ab")
    v3 = ({"r3": 1}, "c")
    v4 = ({"r3": 1}, "c-dup")
    out = siblings([v1, v2, v3, v4])
    assert [val for _, val in out] == ["ab", "c"]
