# Questions

1. Why jitter? Why "full" jitter rather than ±10%?
2. Deadline vs max attempts: why do production RPC systems prefer deadlines?
3. What is retry amplification? Give the number for 4 layers × 3 retries each, and two mitigations.
4. An LLM API returns 429 with a `Retry-After: 20` header. What does your client do?
5. In an agent harness, a tool call times out after it may have charged a customer. Retry or not?

