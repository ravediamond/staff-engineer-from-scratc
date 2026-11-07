import random

from w4d2_bloom import TOMBSTONE, BloomFilter, compact, false_positive_rate, optimal_params


def test_optimal_params():
    m, k = optimal_params(1_000_000, 0.01)
    assert 9_500_000 < m < 9_700_000 and k == 7
    m2, _ = optimal_params(1000, 0.001)
    assert 14_000 < m2 < 14_600


def test_fp_formula():
    assert abs(false_positive_rate(9_585_059, 1_000_000, 7) - 0.01) < 0.0005


def test_no_false_negatives_and_fp_near_target():
    n, p = 5000, 0.02
    m, k = optimal_params(n, p)
    bf = BloomFilter(m, k)
    items = [f"item-{i}" for i in range(n)]
    for x in items:
        bf.add(x)
    assert all(bf.might_contain(x) for x in items)
    fp = sum(bf.might_contain(f"other-{i}") for i in range(20000)) / 20000
    assert fp < 2 * p, fp


def test_compact_newest_wins_and_sorted():
    runs = [
        [("a", "a3"), ("d", TOMBSTONE)],          # newest
        [("a", "a2"), ("b", "b2"), ("d", "d2")],
        [("a", "a1"), ("c", "c1"), ("e", "e1")],  # oldest
    ]
    assert compact(runs, drop_tombstones=True) == [("a", "a3"), ("b", "b2"), ("c", "c1"), ("e", "e1")]
    assert ("d", TOMBSTONE) in compact(runs, drop_tombstones=False)


def test_compact_random_vs_dict():
    rng = random.Random(0)
    runs = []
    for _ in range(6):
        d = {f"k{rng.randint(0, 40):02d}": rng.choice([TOMBSTONE, rng.random()]) for _ in range(15)}
        runs.append(sorted(d.items()))
    expected = {}
    for run in reversed(runs):  # oldest to newest
        expected.update(dict(run))
    exp = sorted((k, v) for k, v in expected.items() if v != TOMBSTONE)
    assert compact(runs, True) == exp
