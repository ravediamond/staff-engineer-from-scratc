import pytest

from w7d2_judge import cohen_kappa, confusion, debiased_verdicts, position_consistency, weighted_kappa


def test_confusion():
    m = confusion(["g", "g", "b", "b"], ["g", "b", "b", "b"], ["g", "b"])
    assert m == [[1, 1], [0, 2]]


def test_kappa_lazy_judge_is_zero():
    human = ["good"] * 90 + ["bad"] * 10
    judge = ["good"] * 100
    assert cohen_kappa(human, judge) == pytest.approx(0.0)


def test_kappa_known_value():
    a = ["y"] * 40 + ["n"] * 60
    b = ["y"] * 30 + ["n"] * 10 + ["y"] * 10 + ["n"] * 50
    po = 0.8
    pe = 0.4 * 0.4 + 0.6 * 0.6
    assert cohen_kappa(a, b) == pytest.approx((po - pe) / (1 - pe))
    assert cohen_kappa(["x"] * 5, ["x"] * 5) == 1.0


def test_weighted_kappa_penalises_far_disagreements():
    labels = [1, 2, 3, 4, 5]
    human = [1, 2, 3, 4, 5] * 20
    near = [min(5, x + 1) for x in human]
    far = [6 - x for x in human]
    assert weighted_kappa(human, human, labels) == pytest.approx(1.0)
    assert weighted_kappa(human, near, labels) > 0.6
    assert weighted_kappa(human, far, labels) < 0
    assert weighted_kappa(human, near, labels) > cohen_kappa(human, near)


def test_position_bias():
    ab = ["A", "A", "B", "tie", "A"]
    ba = ["A", "B", "B", "tie", "B"]
    assert position_consistency(ab, ba) == pytest.approx(0.6)
    assert debiased_verdicts(ab, ba) == ["A", "tie", "B", "tie", "tie"]
