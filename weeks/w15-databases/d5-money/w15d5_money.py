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
        # TODO
        raise NotImplementedError

    def trial_balance(self) -> int:
        """Sum of ALL entries. Must always be 0."""
        # TODO
        raise NotImplementedError

    def transfer(self, key: str, debit: str, credit: str, amount_cents: int) -> bool:
        """Move amount_cents from `debit` to `credit`: two entries, (key, debit, -amount) and (key, credit, +amount).
        Checks, in this order, raising LedgerError and writing NOTHING when one fails:
        1. amount_cents is an int (bool is not accepted) and > 0; debit != credit;
        2. idempotency: if `key` was already used with the SAME (debit, credit, amount): return False and
           change nothing; with different parameters: LedgerError;
        3. if debit is in self.no_overdraft, its balance must stay >= 0.
        Return True when the transfer is recorded."""
        # TODO
        raise NotImplementedError


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
        # TODO
        raise NotImplementedError

    def confirm(self, seat: str, user: str, now: int) -> bool:
        """Sell the seat to the user iff they hold it and the hold has not expired. A second confirm by the
        same user for a seat they already own returns True (idempotent). Otherwise False."""
        # TODO
        raise NotImplementedError


def reconcile(ours: dict[str, int], theirs: dict[str, int]) -> dict:
    """Compare our ledger (payment id -> cents) with the provider's statement.
    Return {"missing_from_ours": sorted ids only they have, "missing_from_theirs": sorted ids only we have,
            "amount_mismatch": sorted ids present in both with different amounts}."""
    # TODO
    raise NotImplementedError
