import pytest

from w5d1_estimation import bandwidth_gbps, human_bytes, llm_gpus, monthly_cost, qps, storage_bytes


def test_qps():
    avg, peak = qps(100e6, 20, 3)
    assert avg == pytest.approx(23148.1, rel=1e-3)
    assert peak == pytest.approx(3 * avg)


def test_storage():
    assert storage_bytes(50e6, 2e6, 5, 3) == pytest.approx(5.475e17)


def test_bandwidth_bits():
    assert bandwidth_gbps(20_000, 50_000) == pytest.approx(8.0)


def test_llm_gpus():
    assert llm_gpus(30, 2000, 400, 20_000, 2_000) == 9
    assert llm_gpus(30, 2000, 400, 20_000, 2_000, headroom=1.3) == 12


def test_cost():
    assert monthly_cost(8, 2.5) == pytest.approx(14_600)
    assert monthly_cost(8, 2.5, 0.5) == pytest.approx(7_300)


def test_human_bytes():
    assert human_bytes(512) == "512 B"
    assert human_bytes(1500) == "1.5 KB"
    assert human_bytes(4e13) == "40.0 TB"
    assert human_bytes(5.475e17) == "547.5 PB"
