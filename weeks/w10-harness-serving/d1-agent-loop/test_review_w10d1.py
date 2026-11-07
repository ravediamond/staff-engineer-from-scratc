from review_w10d1 import run


def test_review_exact_step_budget():
    calls = []
    status, trace = run(lambda t: {"tool": "x"}, lambda a: calls.append(a) or "ok", max_steps=3)
    assert status == "max_steps" and len(calls) == 3
