from review_w4d2 import compact


def test_review_keeps_newest():
    assert compact([[("a", "new")], [("a", "old"), ("b", 1)]]) == [("a", "new"), ("b", 1)]
