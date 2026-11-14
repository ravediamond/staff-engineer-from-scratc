from review_w14d2 import feasible


def test_review_full_nodes_are_not_feasible():
    nodes = [{"name": "a", "gpus": 8, "used_gpus": 8}, {"name": "b", "gpus": 8, "used_gpus": 6},
             {"name": "c", "gpus": 8, "used_gpus": 0}]
    assert feasible(4, nodes) == ["c"]
    assert feasible(2, nodes) == ["b", "c"]
