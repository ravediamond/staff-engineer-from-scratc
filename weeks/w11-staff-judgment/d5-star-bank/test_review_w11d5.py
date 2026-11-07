from review_w11d5 import coverage


def test_review_requires_measurable_result():
    stories = [{"id": "a", "signals": ["influence"], "result": "great success"},
               {"id": "b", "signals": ["influence"], "result": "3 teams adopted it"}]
    assert coverage(stories, ["influence"]) == {"influence": ["b"]}
