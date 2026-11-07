from review_w6d5 import search


def test_review_prefilter():
    scores = {f"c{i}": 1 - i / 100 for i in range(100)}
    acl = {c: ({"ops"} if i >= 90 else {"hr"}) for i, c in enumerate(scores)}
    assert search(scores, acl, {"ops"}, 5) == ["c90", "c91", "c92", "c93", "c94"]
