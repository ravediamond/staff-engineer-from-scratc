"""W2 D3: idempotency store and an exactly-once ledger."""
import hashlib
import json


class InFlight(Exception):
    """409: a request with this key is still executing."""


class KeyConflict(Exception):
    """422: key already used with a different payload."""


def fingerprint(payload: dict) -> str:
    """SHA-256 hex of canonical JSON: sorted keys, separators (',', ':')."""
    # TODO
    raise NotImplementedError


class IdempotencyStore:
    def __init__(self, ttl: float, clock):
        self.ttl, self.clock = ttl, clock
        self.records: dict = {}  # key -> {"fp", "state": "in_flight"|"completed", "result", "at"}
        self.executions = 0

    def execute(self, key: str, payload: dict, fn):
        """Run fn() at most once per (key, payload) within ttl. See README table."""
        # TODO
        raise NotImplementedError


class Ledger:
    def __init__(self, balances: dict, store: IdempotencyStore):
        self.balances = dict(balances)
        self.store = store

    def transfer(self, key: str, src: str, dst: str, amount: int) -> dict:
        """Move amount from src to dst exactly once per key. ValueError on insufficient funds
        (and the key must stay reusable after that failure). Returns {"src": new_src_balance, "dst": new_dst_balance}."""
        # TODO
        raise NotImplementedError
