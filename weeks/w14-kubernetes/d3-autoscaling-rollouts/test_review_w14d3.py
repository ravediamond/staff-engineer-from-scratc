from review_w14d3 import old_pods_to_delete


def test_review_unready_pods_are_not_available():
    assert old_pods_to_delete(10, 1, old=9, new_ready=0, new_unready=3) == 0
    assert old_pods_to_delete(10, 1, old=9, new_ready=3, new_unready=0) == 3
