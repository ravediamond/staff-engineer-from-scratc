# W15 D5: money: ledger, idempotent transfers, holds, reconciliation

Primer: `knowledge/19-databases.md` §5.

## The one idea

Payment, booking and quota systems are asked constantly ("design a wallet", "design ticket booking")
because they punish sloppiness: a lost update is a lost euro. Five rules carry every such design.

1. **Integers, never floats.** Store amounts in the smallest unit (cents) as integers. `0.1 + 0.2 != 0.3`.
2. **Double-entry ledger.** Never update a balance in place. Every movement is a set of **entries**
   that sums to zero (debit one account, credit another), written atomically and **never modified**.
   A balance is derived (sum of entries), so the history explains every number. Corrections are new
   entries (reversals).
3. **Idempotency keys.** The client sends a unique key per intended operation. The same key again
   returns the first result and changes nothing; the same key with different parameters is an error.
   Networks retry; without this you double-charge.
4. **Holds with expiry** for scarce things (seats, stock, card authorisations): `hold → confirm` or
   let it expire. The hold is checked against ONE clock (the database's), not the clocks of app servers.
5. **Reconcile.** Your ledger and the outside world (the bank, the payment provider) drift:
   compare them every day and treat every difference as an incident until explained.

## Today's build (`w15d5_money.py`)

`Ledger` (`transfer`, `balance`, `trial_balance`), `SeatHolds` (`hold`, `confirm`), `reconcile`.

## Staff angle

In a payments design, say "the ledger is append-only and the source of truth; balances are a cache"
and "exactly-once is idempotency keys plus a unique constraint, not a distributed transaction".
For the provider call in the middle (charge the card), describe the state machine and what happens
when the response is lost: you query the provider by your idempotency key before retrying.
