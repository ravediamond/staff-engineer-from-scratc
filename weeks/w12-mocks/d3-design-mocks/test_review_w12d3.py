from review_w12d3 import monthly_human_cost


def test_review_per_month():
    assert monthly_human_cost(1000, 0.1, 5) == 15_000
