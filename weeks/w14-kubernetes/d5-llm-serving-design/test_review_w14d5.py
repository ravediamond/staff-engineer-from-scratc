from review_w14d5 import desired


def test_review_scales_down_when_nothing_waits():
    assert desired(16, {"gpu_util": 0.98, "waiting_per_replica": 0.2}) == 1
    assert desired(4, {"gpu_util": 0.98, "waiting_per_replica": 12.0}) == 12
