from w14d5_serving import (cold_start_seconds, cost_per_million_tokens, desired_replicas, kv_bytes_per_token,
                           max_concurrency, pick_endpoint, simulate)


def test_kv_and_concurrency():
    kv8 = kv_bytes_per_token(32, 8, 128)
    assert kv8 == 131072
    assert kv_bytes_per_token(80, 8, 128) == 327680
    assert max_concurrency(80, 16, 4, 8192, kv8) == 60
    assert max_concurrency(24, 16, 4, 8192, kv8) == 4
    assert max_concurrency(16, 16, 4, 8192, kv8) == 0


def test_cold_start():
    args = dict(node_provision_s=180, image_gb=12, weights_gb=140, pull_gb_s=0.2, download_gb_s=1.0, load_gb_s=2.0)
    assert cold_start_seconds(**args) == 450
    assert cold_start_seconds(**args, node_ready=True, image_cached=True) == 210
    assert cold_start_seconds(**args, node_ready=True, image_cached=True, weights_cached=True) == 70


def test_cost():
    assert abs(cost_per_million_tokens(3, 2000) - 0.4167) < 1e-3
    assert abs(cost_per_million_tokens(3, 2000, utilisation=0.2) - 2.0833) < 1e-3


def pod(name, queue=0, prefixes=(), adapters=(), kv_util=0.3):
    return {"name": name, "queue": queue, "prefixes": set(prefixes), "adapters": set(adapters), "kv_util": kv_util}


def test_endpoint_picker():
    pods = [pod("a", queue=2), pod("b", queue=0), pod("c", queue=3, prefixes=["sys-v2"])]
    assert pick_endpoint(pods, "other", None) == "b", "no affinity: shortest queue"
    assert pick_endpoint(pods, "sys-v2", None) == "c", "a prefix-cache hit is worth a slightly longer queue"
    pods[2]["queue"] = 9
    assert pick_endpoint(pods, "sys-v2", None) == "b", "but not any queue"
    lora = [pod("a", queue=0), pod("b", queue=5, adapters=["legal-fr"])]
    assert pick_endpoint(lora, "x", "legal-fr") == "b", "loading an adapter costs more than waiting"
    assert pick_endpoint(lora, "x", None) == "a"
    full = [pod("a", queue=0, kv_util=0.97), pod("b", queue=4)]
    assert pick_endpoint(full, "x", None) == "b", "a replica with a full KV cache would preempt sequences"
    assert pick_endpoint([pod("b", kv_util=0.99), pod("a", kv_util=0.99)], "x", None) == "a"


def test_desired_replicas_signals():
    assert desired_replicas("queue", 4, 1.0, 8.0) == 8
    assert desired_replicas("queue", 4, 1.0, 0.5) == 1
    assert desired_replicas("util", 4, 1.0, 0.5) == 7, "utilisation says 100% whatever the load"
    assert desired_replicas("queue", 4, 0.0, 100.0) == 16


def test_queue_signal_tracks_load_utilisation_does_not():
    arrivals = [20] * 10 + [120] * 20 + [5] * 60
    by_queue = simulate(arrivals, "queue")
    by_util = simulate(arrivals, "util")
    assert by_util["final_replicas"] == 16, "utilisation stays at 100%: scale to max, never come back"
    assert by_queue["final_replicas"] <= 2
    assert by_queue["replica_ticks"] < 0.6 * by_util["replica_ticks"], "the queue signal costs far less"
    assert by_queue["max_queue"] < 600, "the spike is absorbed after the cold start"
