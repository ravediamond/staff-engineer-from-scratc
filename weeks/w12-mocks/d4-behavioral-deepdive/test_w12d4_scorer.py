import pytest

from w12d4_scorer import decision, normalize, weighted_score

W = {"scope": 2, "influence": 2, "execution": 1, "conflict": 1}


def test_normalize_and_weighted():
    assert normalize({"a": 1, "b": 3}) == {"a": 0.25, "b": 0.75}
    assert weighted_score({"scope": 4, "influence": 3, "execution": 2, "conflict": 3}, W) == pytest.approx(19 / 6)


def test_decision():
    assert decision({"scope": 4, "influence": 4, "execution": 3, "conflict": 3}, W, {}) == "strong hire"
    assert decision({"scope": 3, "influence": 3, "execution": 3, "conflict": 3}, W, {}) == "hire"
    assert decision({"scope": 4, "influence": 2, "execution": 4, "conflict": 4}, W, {"influence": 3}) == "lean no"
    assert decision({"scope": 4, "influence": 1, "execution": 4, "conflict": 4}, W, {"influence": 3}) == "no hire"
    assert decision({"scope": 2, "influence": 2, "execution": 2, "conflict": 2}, W, {}) == "no hire"
