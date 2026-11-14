import math

from w14d4_gpu import QuotaManager, match_devices, place_gang, wasted_fraction, young_daly_interval


def test_gang_is_all_or_nothing():
    free = {"n1": 8, "n2": 8}
    assert place_gang(free, 4, 4) == ["n1", "n1", "n2", "n2"]
    assert free == {"n1": 8, "n2": 8}, "placement is a plan: the caller commits it"
    assert place_gang({"n1": 8, "n2": 4}, 4, 4) is None
    assert place_gang({"n1": 3, "n2": 3, "n3": 2}, 1, 4) is None, "8 free GPUs, none usable: fragmentation"


def test_gang_best_fit_keeps_whole_nodes():
    free = {"a": 8, "b": 2, "c": 4}
    assert place_gang(free, 1, 2) == ["b"]
    assert place_gang(free, 2, 2) == ["b", "c"]
    assert place_gang({"b": 4, "a": 4}, 1, 4) == ["a"]


def wl(name, queue, gpus, priority=0):
    return {"name": name, "queue": queue, "gpus": gpus, "priority": priority}


def test_borrowing_idle_quota():
    qm = QuotaManager({"x": 8, "y": 8})
    assert qm.try_admit(wl("y1", "y", 12)) == (True, []), "y borrows 4 from x's idle quota"
    assert qm.try_admit(wl("y2", "y", 4)) == (True, [])
    assert qm.try_admit(wl("y3", "y", 1)) == (False, []), "cohort is full and y is far above nominal"
    assert qm.used("y") == 16


def test_owner_reclaims_from_borrowers():
    qm = QuotaManager({"x": 8, "y": 8})
    qm.try_admit(wl("y-base", "y", 8, priority=5))
    qm.try_admit(wl("y-low", "y", 4, priority=1))
    qm.try_admit(wl("y-high", "y", 4, priority=9))
    ok, victims = qm.try_admit(wl("x1", "x", 6))
    assert ok and victims == ["y-low", "y-high"], "lowest priority first, until x1 fits"
    assert qm.used("y") == 8 and qm.used("x") == 6
    assert qm.try_admit(wl("x2", "x", 4)) == (False, []), "x would exceed its nominal quota and nothing is free"
    assert qm.try_admit(wl("x3", "x", 2)) == (True, [])


def test_reclaim_never_cuts_into_nominal_and_is_atomic():
    qm = QuotaManager({"x": 4, "y": 4, "z": 4})
    qm.try_admit(wl("y1", "y", 4))
    qm.try_admit(wl("z1", "z", 4))
    qm.try_admit(wl("z2", "z", 4, priority=0))        # z borrows x's quota
    ok, victims = qm.try_admit(wl("x1", "x", 4))
    assert ok and victims == ["z2"]
    qm.release("x1")
    qm.try_admit(wl("y2", "y", 2))                    # y borrows 2
    before = [w["name"] for w in qm.admitted]
    assert qm.try_admit(wl("x-big", "x", 5)) == (False, []), "above x's nominal: no reclaim"
    assert [w["name"] for w in qm.admitted] == before
    ok, victims = qm.try_admit(wl("x2", "x", 4))
    assert ok and victims == ["y2"]
    assert qm.used("y") == 4 and qm.used("z") == 4


def test_same_priority_preempts_most_recent_first():
    qm = QuotaManager({"x": 4, "y": 4})
    qm.try_admit(wl("y1", "y", 4))
    qm.try_admit(wl("y2", "y", 2))
    qm.try_admit(wl("y3", "y", 2))
    assert qm.try_admit(wl("x1", "x", 2)) == (True, ["y3"])


def test_device_claims():
    devs = [{"name": "g0", "model": "A10", "memory_gb": 24, "allocated": False},
            {"name": "g1", "model": "H100", "memory_gb": 80, "allocated": False},
            {"name": "g2", "model": "L40S", "memory_gb": 48, "allocated": False},
            {"name": "g3", "model": "H100", "memory_gb": 80, "allocated": True}]
    assert match_devices(devs, 1, min_memory_gb=40) == ["g2"], "smallest device that satisfies the claim"
    assert match_devices(devs, 2, model="H100") is None and not devs[1]["allocated"]
    assert match_devices(devs, 1, model="H100") == ["g1"]
    assert match_devices(devs, 1) == ["g0"]
    assert match_devices(devs, 1) is None


def test_young_daly():
    tau = young_daly_interval(2, 240)
    assert abs(tau - math.sqrt(960)) < 1e-9
    best = wasted_fraction(tau, 2, 240)
    assert abs(best - 0.129) < 0.001
    assert wasted_fraction(tau / 4, 2, 240) > best and wasted_fraction(tau * 4, 2, 240) > best
