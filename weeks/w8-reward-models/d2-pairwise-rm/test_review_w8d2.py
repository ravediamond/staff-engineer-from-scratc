from review_w8d2 import split


def test_review_prompts_disjoint():
    pairs = [{"prompt_id": p, "i": i} for p in range(50) for i in range(8)]
    tr, te = split(pairs)
    assert not ({x["prompt_id"] for x in tr} & {x["prompt_id"] for x in te})
    assert te
