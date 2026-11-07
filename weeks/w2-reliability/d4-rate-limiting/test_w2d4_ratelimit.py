from w2d4_ratelimit import KeyedLimiter, SlidingWindowCounter, SlidingWindowLog, TokenBucket


def test_token_bucket_burst_then_rate():
    t = [0.0]
    b = TokenBucket(rate=10, capacity=5, clock=lambda: t[0])
    assert sum(b.allow() for _ in range(20)) == 5
    t[0] = 0.5
    assert sum(b.allow() for _ in range(20)) == 5
    t[0] = 0.65  # 1.5 tokens (avoid 0.6 - 0.5 = 0.0999... float trap)
    assert b.allow() and not b.allow()


def test_token_bucket_capped_after_idle():
    t = [0.0]
    b = TokenBucket(rate=10, capacity=100, clock=lambda: t[0])
    t[0] = 3600
    assert sum(b.allow() for _ in range(500)) == 100


def test_token_bucket_cost():
    t = [0.0]
    b = TokenBucket(rate=100, capacity=1000, clock=lambda: t[0])
    assert b.allow(800) and not b.allow(300)
    t[0] = 1.0
    assert b.allow(300)


def test_sliding_log_exact():
    t = [0.0]
    lim = SlidingWindowLog(limit=3, window=10, clock=lambda: t[0])
    results = []
    for ts in [0, 1, 2, 3, 9.9, 10, 10.5, 11, 12, 12.1]:
        t[0] = ts
        results.append(lim.allow())
    assert results == [True, True, True, False, False, True, False, True, True, False]


def test_sliding_counter_weighting():
    t = [0.0]
    lim = SlidingWindowCounter(limit=10, window=60, clock=lambda: t[0])
    t[0] = 30
    assert sum(lim.allow() for _ in range(15)) == 10
    t[0] = 90  # half way into next window: estimate = 10 * 0.5 + curr
    assert sum(lim.allow() for _ in range(15)) == 5
    t[0] = 200  # two windows later: nothing carries over
    assert sum(lim.allow() for _ in range(15)) == 10


def test_keyed():
    t = [0.0]
    k = KeyedLimiter(lambda: TokenBucket(rate=1, capacity=2, clock=lambda: t[0]))
    assert k.allow("a") and k.allow("a") and not k.allow("a")
    assert k.allow("b"), "keys are independent"
