from review_w3d2 import quorum_read


def test_review_returns_newest():
    replicas = [{"p": (1, "old")}, {"p": (2, "new")}, {"p": (2, "new")}]
    assert quorum_read(replicas, "p", 2) == "new"
