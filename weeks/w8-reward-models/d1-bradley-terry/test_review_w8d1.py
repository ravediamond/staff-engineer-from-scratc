from review_w8d1 import fit


def test_review_winner_ranks_higher():
    r = fit(3, [(0, 1)] * 10 + [(1, 2)] * 10 + [(0, 2)] * 10)
    assert r[0] > r[1] > r[2]
