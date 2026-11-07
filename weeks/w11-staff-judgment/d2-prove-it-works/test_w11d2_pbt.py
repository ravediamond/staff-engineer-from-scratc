import random

from w11d2_pbt import check, dedupe_sorted_buggy, gen_int, gen_list, minimize, shrink_int, shrink_list


def test_generators():
    rng = random.Random(0)
    xs = [gen_int(rng, -3, 3) for _ in range(500)]
    assert min(xs) == -3 and max(xs) == 3
    ls = [gen_list(rng, lambda r: 1, 4) for _ in range(200)]
    assert {len(l) for l in ls} == {0, 1, 2, 3, 4}


def test_shrinkers():
    assert shrink_int(10) == [0, 5, 9]
    assert shrink_int(-7) == [0, -3, -6]
    assert shrink_int(1) == [0]
    assert shrink_int(0) == []
    c = shrink_list([3, 1], shrink_int)
    assert c[:3] == [[], [3], [1]]
    assert [0, 1] in c and [3, 0] in c and [3, 1] not in c


def test_minimize_sum():
    fails = lambda xs: sum(xs) >= 100
    m = minimize([37, 80, 12], fails, lambda xs: shrink_list(xs, shrink_int))
    assert sum(m) == 100 and len(m) <= 2


def test_check_finds_minimal_dedupe_bug():
    def prop(xs):
        s = sorted(xs)
        out = dedupe_sorted_buggy(s)
        return out == sorted(set(s))

    gen = lambda rng: gen_list(rng, lambda r: gen_int(r, 0, 3), 8)
    cex = check(prop, gen, lambda xs: shrink_list(xs, shrink_int), n=300, seed=1)
    assert len(cex) == 3 and len(set(cex)) == 1, cex  # three equal values: the minimal shape of the bug


def test_check_returns_none_when_property_holds():
    gen = lambda rng: gen_list(rng, lambda r: gen_int(r, -5, 5), 6)
    assert check(lambda xs: sorted(sorted(xs)) == sorted(xs), gen, lambda xs: shrink_list(xs, shrink_int)) is None
