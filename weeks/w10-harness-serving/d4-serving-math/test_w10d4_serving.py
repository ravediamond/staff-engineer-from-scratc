import random

import pytest

from w10d4_serving import contiguous_waste, kv_bytes_per_token, kv_cache_bytes, max_concurrent, paged_waste, simulate


def test_kv_math():
    assert kv_bytes_per_token(32, 8, 128) == 131_072
    assert kv_cache_bytes(32, 8, 128, 32_768, 1) == 4 * 2 ** 30
    assert max_concurrent(80, 16, 131_072, 2048) == 238


def test_static_vs_continuous_simple():
    reqs = [(0, 10), (0, 10), (0, 10), (0, 500), (0, 10), (0, 10)]
    st = simulate(reqs, 4, "static")
    co = simulate(reqs, 4, "continuous")
    assert st["makespan"] == 510 and co["makespan"] == 500
    assert co["mean_latency"] < st["mean_latency"]


def test_continuous_wins_on_random_traffic():
    rng = random.Random(0)
    reqs, t = [], 0
    for _ in range(300):
        t += rng.randint(0, 3)
        reqs.append((t, rng.choice([5, 20, 50, 400])))
    st = simulate(reqs, 16, "static")
    co = simulate(reqs, 16, "continuous")
    assert co["throughput"] > st["throughput"]
    assert co["mean_latency"] < 0.5 * st["mean_latency"]


def test_idle_and_latency():
    out = simulate([(5, 3)], 4, "continuous")
    assert out["makespan"] == 8 and out["mean_latency"] == 3


def test_waste():
    lens = [100, 1500, 30, 4000]
    assert contiguous_waste(lens, 4096) == 4 * 4096 - sum(lens)
    assert paged_waste(lens, 16) == (112 - 100) + (1504 - 1500) + (32 - 30) + 0
    assert paged_waste(lens, 16) < 16 * len(lens)
