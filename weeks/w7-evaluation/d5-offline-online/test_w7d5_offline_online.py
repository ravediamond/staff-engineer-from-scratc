import pytest

from w7d5_offline_online import average_ranks, kendall_tau, launch_decision, sign_agreement, spearman


def test_kendall():
    assert kendall_tau([1, 2, 3, 4, 5], [1, 3, 2, 4, 5]) == pytest.approx(0.8)
    assert kendall_tau([1, 2, 3], [3, 2, 1]) == pytest.approx(-1.0)
    assert kendall_tau([1, 1, 2], [1, 2, 3]) == pytest.approx(2 / 3)


def test_ranks_and_spearman():
    assert average_ranks([10, 20, 20, 5]) == [2.0, 3.5, 3.5, 1.0]
    assert spearman([1, 2, 3, 4], [10, 20, 30, 40]) == pytest.approx(1.0)
    assert spearman([1, 2, 3, 4, 5], [5, 6, 7, 8, 7]) == pytest.approx(0.82078, abs=1e-4)


def test_sign_agreement():
    assert sign_agreement([(0.02, 0.01), (0.03, -0.01), (-0.01, -0.02), (0.0, 0.5)]) == pytest.approx(2 / 3)


def test_launch_rules():
    assert launch_decision((0.01, 0.03), (0.002, 0.01), []) == "ship"
    assert launch_decision((0.01, 0.03), (-0.01, 0.01), []) == "iterate"
    assert launch_decision((0.01, 0.03), (-0.02, -0.001), []) == "rollback"
    assert launch_decision((0.01, 0.03), (0.002, 0.01), ["latency_p95"]) == "rollback"
