# Questions

1. Define idempotent. Which HTTP methods are idempotent by spec?
2. Why does "exactly-once delivery" not exist, and what do systems that advertise it actually do?
3. Walk through the idempotency-key table. Why the fingerprint check?
4. The effect is an external API (send email) and your idempotency store is Postgres. Where can it still double-send, and how do you narrow it?
5. In an agent harness, how do you derive idempotency keys for tool calls, and what does replay look like?

## Model answers

1. Applying it N times has the same effect as once. By spec GET, HEAD, PUT, DELETE, OPTIONS are idempotent; POST and PATCH are not. (Idempotent ≠ safe: DELETE changes state.)
2. A sender cannot distinguish "message lost" from "ack lost" (Two Generals), so it must resend, and the receiver may get duplicates. "Exactly-once" systems (Kafka EOS, Flink) do at-least-once plus deduplication or transactional commit of output together with input offsets.
3. Absent → execute. In-flight → 409. Completed with same fingerprint → replay the stored response without re-executing. Completed with a different fingerprint → 422. Failure → release the key. The fingerprint check catches client bugs that reuse keys, which would otherwise return a wrong receipt and silently drop the second operation.
4. Crash after the email is sent but before the record is marked completed: the retry sends again. Narrow it by passing your idempotency key to the provider (many support it), by using an outbox (write "intent to send" in the same transaction as the business change, then a relay sends and marks done, accepting at-least-once to a provider that dedupes), or by recording "sent" before the effect and accepting at-most-once.
5. Key = hash(run_id, step_index, tool_name, canonical args). On retry or replay of the same step, the executor finds the completed record and returns the recorded output without re-executing, which is also what makes deterministic replay of traces possible (W10 D3). Read-only tools can skip it; any tool with side effects must have it.
