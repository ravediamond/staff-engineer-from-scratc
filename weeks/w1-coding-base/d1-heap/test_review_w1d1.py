import random

from review_w1d1 import heap_pop, heap_push


def test_review_pop_order():
    rng = random.Random(0)
    for _ in range(50):
        xs = [rng.randint(0, 100) for _ in range(rng.randint(1, 40))]
        h = []
        for x in xs:
            heap_push(h, x)
        assert [heap_pop(h) for _ in xs] == sorted(xs)
