from w14d2_scheduler import eviction_order, filter_nodes, qos_class, schedule, score


def node(name, cpu=8, mem=32, used_cpu=0, used_mem=0, labels=None, taints=None):
    return {"name": name, "cpu": cpu, "mem": mem, "used_cpu": used_cpu, "used_mem": used_mem,
            "labels": labels or {}, "taints": taints or []}


def pod(name="p", cpu=1, mem=1, node_selector=None, tolerations=None):
    return {"name": name, "cpu": cpu, "mem": mem, "node_selector": node_selector or {}, "tolerations": tolerations or []}


def test_filter_uses_requests_not_capacity():
    nodes = [node("a", used_cpu=7), node("b", used_cpu=6), node("c", used_mem=31.5)]
    assert filter_nodes(pod(cpu=2, mem=1), nodes) == ["b"]
    assert filter_nodes(pod(cpu=1, mem=1), nodes) == ["a", "b"]


def test_taints_and_selectors():
    nodes = [node("cpu-1"), node("gpu-1", labels={"pool": "gpu"}, taints=[("gpu", "true")])]
    assert filter_nodes(pod(), nodes) == ["cpu-1"], "an untolerated taint repels"
    train = pod(tolerations=[("gpu", "true")])
    assert filter_nodes(train, nodes) == ["cpu-1", "gpu-1"], "a toleration permits, it does not attract"
    train["node_selector"] = {"pool": "gpu"}
    assert filter_nodes(train, nodes) == ["gpu-1"]


def test_score_spread_vs_binpack():
    empty, half = node("empty"), node("half", used_cpu=4, used_mem=16)
    p = pod(cpu=2, mem=8)
    assert score(p, empty, "spread") == 75.0 and score(p, half, "spread") == 25.0
    assert score(p, empty, "binpack") == 25.0 and score(p, half, "binpack") == 75.0


def test_schedule_binds_and_accounts():
    nodes = [node("a"), node("b")]
    placed = [schedule(pod(f"p{i}", cpu=2, mem=8), nodes, "spread") for i in range(4)]
    assert placed == ["a", "b", "a", "b"]
    assert nodes[0]["used_cpu"] == 4 and nodes[0]["used_mem"] == 16
    nodes = [node("a"), node("b")]
    placed = [schedule(pod(f"p{i}", cpu=2, mem=8), nodes, "binpack") for i in range(5)]
    assert placed == ["a", "a", "a", "a", "b"]
    full = [node("a", used_cpu=8)]
    assert schedule(pod(), full) is None and full[0]["used_cpu"] == 8


def test_binpack_keeps_room_for_a_big_pod():
    for strategy, expect_big in (("spread", None), ("binpack", "b")):
        nodes = [node("a"), node("b")]
        for i in range(4):
            schedule(pod(f"s{i}", cpu=2, mem=4), nodes, strategy)
        assert schedule(pod("big", cpu=8, mem=8), nodes, strategy) == expect_big


def test_qos_class():
    assert qos_class([{}]) == "BestEffort"
    assert qos_class([{"requests": {"cpu": 0.5, "mem": 1}, "limits": {"cpu": 0.5, "mem": 1}}]) == "Guaranteed"
    assert qos_class([{"limits": {"cpu": 1, "mem": 2}}]) == "Guaranteed", "requests default to limits"
    assert qos_class([{"requests": {"cpu": 0.5, "mem": 1}, "limits": {"cpu": 0.5, "mem": 2}}]) == "Burstable"
    assert qos_class([{"requests": {"cpu": 0.5}}]) == "Burstable"
    assert qos_class([{"limits": {"cpu": 1, "mem": 2}}, {}]) == "Burstable", "one container without limits is enough"
    assert qos_class([{"limits": {"mem": 2}}]) == "Burstable"


def test_eviction_order():
    pods = [{"name": "guaranteed", "mem_usage": 4, "mem_request": 4},
            {"name": "burst-over", "mem_usage": 6, "mem_request": 2},
            {"name": "burst-under", "mem_usage": 1, "mem_request": 4},
            {"name": "besteffort", "mem_usage": 3, "mem_request": 0}]
    assert eviction_order(pods) == ["burst-over", "besteffort", "guaranteed", "burst-under"]
