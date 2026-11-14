# Questions

1. Why a double-entry, append-only ledger instead of a `balance` column? What do you gain and what does it cost?
2. Design the idempotency of `POST /transfers`: key, storage, scope, expiry, and the race between two concurrent retries.
3. Your service calls a payment provider and the response times out. What state are you in, and what do you do?
4. Ticket booking for a 50,000-seat concert that sells out in a minute: the hard part and your design for it.
5. What does reconciliation catch that tests cannot? How often, and what happens with a difference?
6. Where do you need a distributed transaction, and what do you use instead (saga, outbox, TCC)?

