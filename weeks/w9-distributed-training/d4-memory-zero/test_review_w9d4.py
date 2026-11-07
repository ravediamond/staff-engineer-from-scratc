from review_w9d4 import bytes_per_param_mixed_adam, fits_ddp


def test_review_sixteen_bytes():
    assert bytes_per_param_mixed_adam() == 16
    assert not fits_ddp(5e9, 80e9, 5e9)
