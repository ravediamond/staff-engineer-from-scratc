from review_w7d3 import mcnemar_chi2, p_value


def test_review_only_discordant_pairs():
    chi2 = mcnemar_chi2(both_pass=900, a_only=40, b_only=10, both_fail=50)
    assert abs(chi2 - 29 ** 2 / 50) < 1e-9
    assert p_value(chi2) < 0.001
