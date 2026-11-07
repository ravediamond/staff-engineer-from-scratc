# Questions

1. Token bucket vs leaky bucket vs sliding window: one sentence each, and when you pick each.
2. Why compute refills lazily instead of a timer per key?
3. Design rate limiting for an LLM API gateway: 50k customers, limits in requests AND tokens per minute, 20 gateway instances.
4. Your limiter uses Redis. Redis is down. Fail open or fail closed? Defend it.
5. Why is limiting on requests the wrong unit for LLM traffic, and how do you charge tokens you do not know yet?

