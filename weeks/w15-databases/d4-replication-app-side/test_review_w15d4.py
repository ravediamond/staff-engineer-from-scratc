from review_w15d4 import pick_node


def test_review_read_your_writes_routing():
    replicas = {"r1": {"healthy": True, "applied_lsn": 90}, "r2": {"healthy": True, "applied_lsn": 100},
                "r3": {"healthy": False, "applied_lsn": 200}}
    assert pick_node(replicas, 95) == "r2"
    assert pick_node(replicas, 50) == "r1"
    assert pick_node(replicas, 150) == "primary"
