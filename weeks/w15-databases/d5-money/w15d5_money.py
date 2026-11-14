"""W15 D5: double-entry ledger with idempotent transfers, seat holds with expiry, reconciliation."""


class LedgerError(Exception):
    pass


class Ledger:
    def __init__(self):
        self.entries: list[tuple[str, str, int]] = []       # (transfer id, account, signed amount in cents)
        self.requests: dict[str, tuple] = {}                 # idempotency key -> (debit, credit, amount)
        self.no_overdraft: set[str] = set()                  # accounts whose balance may not go below zero

    def balance(self, account: str) -> int:
        """Sum of the account's entries (0 if none)."""
        return sum(amount for _, acct, amount in self.entries if acct == account)

    def trial_balance(self) -> int:
        """Sum of ALL entries. Must always be 0."""
        return sum(amount for _, _, amount in self.entries)

    def transfer(self, key: str, debit: str, credit: str, amount_cents: int) -> bool:
        """Move amount_cents from `debit` to `credit`: two entries, (key, debit, -amount) and (key, credit, +amount).
        Checks, in this order, raising LedgerError and writing NOTHING when one fails:
        1. amount_cents is an int (bool is not accepted) and > 0; debit != credit;
        2. idempotency: if `key` was already used with the SAME (debit, credit, amount): return False and
           change nothing; with different parameters: LedgerError;
        3. if debit is in self.no_overdraft, its balance must stay >= 0.
        Return True when the transfer is recorded."""
        if type(amount_cents) is not int or amount_cents <= 0:
            raise LedgerError("amount must be a positive integer number of cents")
        if debit == credit:
            raise LedgerError("debit and credit accounts must differ")
        params = (debit, credit, amount_cents)
        if key in self.requests:
            if self.requests[key] != params:
                raise LedgerError("idempotency key reused with different parameters")
            return False
        if debit in self.no_overdraft and self.balance(debit) - amount_cents < 0:
            raise LedgerError("insufficient funds")
        self.requests[key] = params
        self.entries.append((key, debit, -amount_cents))
        self.entries.append((key, credit, amount_cents))
        return True


class SeatHolds:
    """Seats are held for `ttl` seconds, then confirmed (sold) or released by expiry.
    `now` is always passed in by the caller: in production it is the DATABASE's clock, one source of truth."""

    def __init__(self, ttl: int = 120):
        self.ttl = ttl
        self.holds: dict[str, tuple[str, int]] = {}      # seat -> (user, expires_at)
        self.sold: dict[str, str] = {}                   # seat -> user

    def hold(self, seat: str, user: str, now: int) -> bool:
        """True if the user now holds the seat. Refuse (False) if the seat is sold, or held by ANOTHER user
        and not expired (a hold is expired when now >= expires_at). The same user holding again renews it."""
        if seat in self.sold:
            return False
        current = self.holds.get(seat)
        if current is not None and current[0] != user and now < current[1]:
            return False
        self.holds[seat] = (user, now + self.ttl)
        return True

    def confirm(self, seat: str, user: str, now: int) -> bool:
        """Sell the seat to the user iff they hold it and the hold has not expired. A second confirm by the
        same user for a seat they already own returns True (idempotent). Otherwise False."""
        if self.sold.get(seat) == user:
            return True
        current = self.holds.get(seat)
        if seat in self.sold or current is None or current[0] != user or now >= current[1]:
            return False
        self.sold[seat] = user
        del self.holds[seat]
        return True


def reconcile(ours: dict[str, int], theirs: dict[str, int]) -> dict:
    """Compare our ledger (payment id -> cents) with the provider's statement.
    Return {"missing_from_ours": sorted ids only they have, "missing_from_theirs": sorted ids only we have,
            "amount_mismatch": sorted ids present in both with different amounts}."""
    return {"missing_from_ours": sorted(set(theirs) - set(ours)),
            "missing_from_theirs": sorted(set(ours) - set(theirs)),
            "amount_mismatch": sorted(k for k in set(ours) & set(theirs) if ours[k] != theirs[k])}
