import random

import pytest

from w7d1_harness import flaky, gate, paired_bootstrap, run_eval, slice_means


def make_cases(n=300, seed=0):
    rng = random.Random(seed)
    return [{"id": f"c{i}", "input": i, "expected": None, "slice": "fr" if i % 10 == 0 else "en",
             "difficulty": rng.random()} for i in range(n)]


def test_run_eval_repeats_and_flaky():
    cases = make_cases(10)

    def system(x, r):
        return 1.0 if x % 3 else float(r % 2)  # every third case flips between repeats

    res = run_eval(cases, system, lambda out, exp: out, repeats=4)
    assert res["c1"] == (1.0, 0.0)
    assert res["c0"] == (0.5, 0.5)
    assert flaky(res) == ["c0", "c3", "c6", "c9"]


def test_slice_means():
    cases = make_cases(20)
    scores = {c["id"]: (1.0 if c["slice"] == "fr" else 0.5) for c in cases}
    assert slice_means(scores, cases) == {"fr": 1.0, "en": 0.5}


def test_paired_bootstrap_detects_small_consistent_gain():
    cases = make_cases()
    base = {c["id"]: c["difficulty"] for c in cases}
    new = {k: v + 0.02 for k, v in base.items()}
    d, lo, hi = paired_bootstrap(base, new, 1000, 0)
    assert d == pytest.approx(0.02) and lo > 0.019 and hi < 0.021


def test_gate_reasons():
    cases = make_cases()
    base = {c["id"]: c["difficulty"] for c in cases}
    same = dict(base)
    assert gate(base, same, cases, 0.01, 0.05)["pass"]
    worse_fr = {c["id"]: (c["difficulty"] - 0.2 if c["slice"] == "fr" else c["difficulty"]) for c in cases}
    g = gate(base, worse_fr, cases, max_drop=0.05, slice_max_drop=0.05)
    assert not g["pass"] and g["reasons"] == ["significant regression", "slice fr"]
    much_worse = {k: v - 0.1 for k, v in base.items()}
    g = gate(base, much_worse, cases, 0.05, 0.5)
    assert g["reasons"] == ["significant regression", "mean drop"]
