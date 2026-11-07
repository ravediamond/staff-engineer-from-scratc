from review_w11d4 import Controller


def test_review_gate_on_threshold():
    c = Controller(threshold=0.001)
    c.record_verification(0.04)
    assert c.cutover() == "old"
    c.record_verification(0.0002)
    assert c.cutover() == "new"
