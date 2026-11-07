import random
from collections import Counter

from w12d2_mock import ladder_length, misra_gries


def test_misra_gries_small():
    assert misra_gries("abacabda", 2) == {"a": 2}


def test_misra_gries_guarantees():
    rng = random.Random(0)
    for _ in range(50):
        k = rng.randint(1, 6)
        stream = [rng.choice("aaaabbbcdefghij") for _ in range(rng.randint(10, 400))]
        n, true = len(stream), Counter(stream)
        c = misra_gries(stream, k)
        assert len(c) <= k
        for x, f in true.items():
            est = c.get(x, 0)
            assert f - n / (k + 1) <= est <= f
            if f > n / (k + 1):
                assert x in c


def test_ladder():
    assert ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]) == 5
    assert ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log"]) == 0
    assert ladder_length("a", "c", ["a", "b", "c"]) == 2
