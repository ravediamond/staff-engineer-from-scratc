from review_w13d3 import Coordinator


def test_review_zombie_commit_is_rejected():
    c = Coordinator()
    g1 = c.assign({0: "slow"})
    assert c.commit("slow", g1, 0, 100)
    g2 = c.assign({0: "fast"})          # "slow" timed out, partition 0 moved
    assert c.commit("fast", g2, 0, 5000)
    assert not c.commit("slow", g1, 0, 150), "a commit from an old generation must be refused"
    assert c.committed[0] == 5000
    assert not c.commit("slow", g2, 0, 150), "even with the right generation, only the owner commits"
