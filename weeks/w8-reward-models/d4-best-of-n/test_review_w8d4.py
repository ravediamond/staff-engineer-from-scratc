from review_w8d4 import bon_report


def test_review_evaluate_with_independent_judge():
    groups = [[{"rm": 0.9, "true": 0.2}, {"rm": 0.4, "true": 0.6}]]
    out = bon_report(groups, lambda r: r["rm"], lambda r: r["true"])
    assert out == 0.2
