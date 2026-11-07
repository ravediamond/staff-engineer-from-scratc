# Questions

1. Define idempotent. Which HTTP methods are idempotent by spec?
2. Why does "exactly-once delivery" not exist, and what do systems that advertise it actually do?
3. Walk through the idempotency-key table. Why the fingerprint check?
4. The effect is an external API (send email) and your idempotency store is Postgres. Where can it still double-send, and how do you narrow it?
5. In an agent harness, how do you derive idempotency keys for tool calls, and what does replay look like?

