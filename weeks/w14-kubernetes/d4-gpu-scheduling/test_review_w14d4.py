from review_w14d4 import admit


def test_review_failed_admission_holds_nothing():
    free = {"n1": 8, "n2": 4}
    assert admit(free, 4, 4) is False
    assert free == {"n1": 8, "n2": 4}, "a job that cannot start must not keep GPUs"
    assert admit(free, 3, 4) is True
    assert free == {"n1": 0, "n2": 0}
