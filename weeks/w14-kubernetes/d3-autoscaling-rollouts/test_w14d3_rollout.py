from w14d3_rollout import Stabilizer, drain_plan, hpa_desired, rollout_step


def test_hpa_formula():
    assert hpa_desired(4, 90, 60, 1, 20) == 6
    assert hpa_desired(10, 57, 60, 1, 20) == 10, "inside the tolerance"
    assert hpa_desired(10, 65, 60, 1, 20) == 10
    assert hpa_desired(10, 67, 60, 1, 20) == 12
    assert hpa_desired(10, 20, 60, 1, 20) == 4
    assert hpa_desired(10, 300, 60, 1, 20) == 20 and hpa_desired(3, 1, 60, 2, 20) == 2
    assert hpa_desired(3, 61, 30, 1, 20) == 7, "ceil, not round"


def test_stabilizer_scales_up_now_and_down_late():
    s = Stabilizer(window=300)
    assert s.recommend(0, 10) == 10
    assert s.recommend(60, 4) == 10
    assert s.recommend(120, 12) == 12, "scale-up is immediate"
    assert s.recommend(300, 4) == 12
    assert s.recommend(420, 4) == 12, "the entry at t=120 is exactly at the edge of the window"
    assert s.recommend(421, 4) == 4


def simulate(desired, surge, unavail, becomes_ready=True, steps=50):
    old, ready, unready = desired, 0, 0
    for _ in range(steps):
        create, delete = rollout_step(desired, surge, unavail, old, ready, unready)
        assert 0 <= delete <= old and create >= 0
        old -= delete
        unready += create
        assert old + ready + unready <= desired + surge, "too many pods"
        assert old + ready >= desired - unavail, "too few available pods"
        assert ready + unready <= desired
        if becomes_ready:
            ready, unready = ready + unready, 0
        if old == 0 and ready == desired:
            break
    return old, ready, unready


def test_rollout_completes_within_bounds():
    for desired, surge, unavail in [(10, 2, 1), (10, 3, 0), (10, 0, 1), (4, 1, 1), (1, 1, 0)]:
        assert simulate(desired, surge, unavail) == (0, desired, 0), (desired, surge, unavail)


def test_first_step_values():
    assert rollout_step(10, 2, 1, old=10, new_ready=0, new_unready=0) == (2, 1)
    assert rollout_step(10, 0, 1, old=10, new_ready=0, new_unready=0) == (0, 1)
    assert rollout_step(10, 3, 0, old=10, new_ready=0, new_unready=0) == (3, 0)


def test_broken_image_stalls_without_outage():
    old, ready, unready = simulate(10, 2, 1, becomes_ready=False)
    assert ready == 0 and old == 9 and unready == 3, "9 old pods keep serving; new ones wait for readiness"


def test_drain_respects_pdb():
    ready = {"api": 3, "worker": 5, "db": 1}
    budgets = {"api": 2, "db": 1}
    evicted, blocked = drain_plan(["api", "api", "worker", "db", "worker"], ready, budgets)
    assert evicted == ["api", "worker", "worker"] and blocked == ["api", "db"]
    assert ready == {"api": 3, "worker": 5, "db": 1}, "inputs must not be modified"
