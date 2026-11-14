from review_w13d4 import watermark


def test_review_slow_partition_holds_the_watermark():
    assert watermark([3600, 3590, 1200], 30) == 1170
    assert watermark([3600, None, 3590], 30) is None
