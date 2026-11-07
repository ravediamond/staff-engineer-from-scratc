"""Self-contained arithmetic + tiny simulation. Run after predict.md."""
print("1. no breaker: every request during the outage waits the full timeout ->", 60 * 100, "requests x 2 s")
reached, t, state, opened_at, fails = 0, 0.0, "closed", 0.0, 0
while t < 60:
    if state == "open" and t >= opened_at + 5:
        state = "half"
    if state == "closed" or state == "half":
        reached += 1
        fails += 1
        if state == "half" or fails >= 5:
            state, opened_at, fails = "open", t, 0
    t += 0.01
print("2. with breaker: requests that reach the dead dependency:", reached, "(5 to trip, then 1 probe every 5 s)")
print("3. unlimited half-open: all 100 req/s pass at once -> the fragile service falls over again -> flapping.")
