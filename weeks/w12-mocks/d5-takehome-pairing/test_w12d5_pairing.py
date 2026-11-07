from w12d5_pairing import TransientError, run_all, run_case, run_case_with_retry, slice_report

CASES = [{"id": "c1", "input": 1, "expected": 2, "slice": "en"},
         {"id": "c2", "input": 2, "expected": 4, "slice": "en"},
         {"id": "c3", "input": 3, "expected": 7, "slice": "fr"}]


def flaky_system(fail_times):
    calls = {}

    def system(x):
        calls[x] = calls.get(x, 0) + 1
        if calls[x] <= fail_times:
            raise TransientError("503")
        return 2 * x

    return system, calls


def test_existing_behaviour_unchanged():
    out = run_all(lambda x: 2 * x, CASES)
    assert out["mean"] == 2 / 3 and "slices" not in out
    assert run_case(lambda x: 1 / 0, CASES[0])["error"].startswith("ZeroDivisionError")


def test_retry_only_transient():
    system, calls = flaky_system(2)
    r = run_case_with_retry(system, CASES[0], retries=2)
    assert r["score"] == 1.0 and r["attempts"] == 3 and r["error"] is None
    system, _ = flaky_system(5)
    r = run_case_with_retry(system, CASES[0], retries=2)
    assert r["attempts"] == 3 and r["error"] == "TransientError: 503"
    n = [0]

    def buggy(x):
        n[0] += 1
        raise KeyError("x")

    r = run_case_with_retry(buggy, CASES[0], retries=5)
    assert n[0] == 1 and r["attempts"] == 1 and r["error"].startswith("KeyError")


def test_slices_and_wiring():
    system, _ = flaky_system(1)
    out = run_all(system, CASES, retries=1, by_slice=True)
    assert out["slices"] == {"en": {"n": 2, "mean": 1.0, "errors": 0}, "fr": {"n": 1, "mean": 0.0, "errors": 0}}
    assert all(r["attempts"] == 2 for r in out["results"])
    rep = slice_report([{"id": "c3", "score": 0.0, "error": "boom"}], CASES)
    assert rep == {"fr": {"n": 1, "mean": 0.0, "errors": 1}}
