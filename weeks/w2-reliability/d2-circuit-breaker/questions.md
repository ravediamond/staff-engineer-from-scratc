# Questions

1. Draw the state machine. Why is half-open needed at all?
2. Why split `allow()` from `record_*()` instead of only offering `call(fn)`?
3. Consecutive-failure threshold vs error-rate-over-window: when does each misbehave?
4. Your breaker opens on a dependency, and the product shows 500s. What did the design miss?
5. Breakers per instance vs shared across the fleet: trade-offs.

