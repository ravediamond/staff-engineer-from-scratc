import math
import random

from w11d1_rootcause import bisect_first_bad, change_point, last_event_before, majority


def test_majority():
    assert majority([True, True, False]) and not majority([True, False]) and not majority([])


def test_bisect_deterministic():
    for bad in [1, 2, 500, 998, 999]:
        idx, calls = bisect_first_bad(1000, lambda i: i >= bad)
        assert idx == bad
        assert calls <= math.ceil(math.log2(1000))


def test_bisect_flaky_with_repeats():
    rng = random.Random(0)
    bad = 613

    def success_rate(repeats):
        ok = 0
        for _ in range(200):
            def is_bad(i):
                return True if i >= bad else rng.random() < 0.2  # 20% false alarms on good versions
            ok += bisect_first_bad(1000, is_bad, repeats=repeats)[0] == bad
        return ok / 200

    one, fifteen = success_rate(1), success_rate(15)
    assert one < 0.5, "one run per probe with a 20% flake usually blames the wrong version"
    assert fifteen >= 0.92, fifteen


def test_change_point_and_events():
    series = [100, 102, 98, 101, 99, 100, 103, 97, 100, 101, 104, 99, 160, 170, 165]
    i = change_point(series, baseline_n=10, k=3)
    assert i == 12
    assert change_point([1, 1, 2, 1, 2, 1], 3) is None
    deploys = [(3, "v41"), (11, "v42"), (14, "v43")]
    assert last_event_before(12, deploys) == (11, "v42")
    assert last_event_before(1, deploys) is None
