import pytest

from w12d3_capacity import online_store_size, serving_qps, triage_cost_per_month


def test_store_and_qps():
    assert online_store_size(200e6, 300, 8, 3) == pytest.approx(1.44e12)
    assert serving_qps(20_000, 300, False) == 6e6
    assert serving_qps(20_000, 300, True) == 20_000


def test_triage_cost():
    c = triage_cost_per_month(50_000, 1500, 200, 1, 5, 0.25, 4)
    assert c["llm"] == pytest.approx(3750)
    assert c["human"] == pytest.approx(1_500_000)
    assert c["total"] == pytest.approx(1_503_750)
