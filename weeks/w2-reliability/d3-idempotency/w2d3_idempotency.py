"""W2 D3: idempotency store and an exactly-once ledger."""
import hashlib
import json


class InFlight(Exception):
    """409: a request with this key is still executing."""


class KeyConflict(Exception):
    """422: key already used with a different payload."""


def fingerprint(payload: dict) -> str:
    """SHA-256 hex of canonical JSON: sorted keys, separators (',', ':')."""
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode()).hexdigest()


class IdempotencyStore:
    def __init__(self, ttl: float, clock):
        self.ttl, self.clock = ttl, clock
        self.records: dict = {}  # key -> {"fp", "state": "in_flight"|"completed", "result", "at"}
        self.executions = 0

    def execute(self, key: str, payload: dict, fn):
        """Run fn() at most once per (key, payload) within ttl. See README table."""
        now = self.clock()
        fp = fingerprint(payload)
        rec = self.records.get(key)
        if rec is not None and now - rec["at"] >= self.ttl:
            del self.records[key]
            rec = None
        if rec is not None:
            if rec["fp"] != fp:
                raise KeyConflict(key)
            if rec["state"] == "in_flight":
                raise InFlight(key)
            return rec["result"]
        self.records[key] = {"fp": fp, "state": "in_flight", "result": None, "at": now}
        try:
            self.executions += 1
            result = fn()
        except Exception:
            del self.records[key]
            raise
        self.records[key].update(state="completed", result=result, at=self.clock())
        return result


class Ledger:
    def __init__(self, balances: dict, store: IdempotencyStore):
        self.balances = dict(balances)
        self.store = store

    def transfer(self, key: str, src: str, dst: str, amount: int) -> dict:
        """Move amount from src to dst exactly once per key. ValueError on insufficient funds
        (and the key must stay reusable after that failure). Returns {"src": new_src_balance, "dst": new_dst_balance}."""
        def effect():
            if amount <= 0 or self.balances[src] < amount:
                raise ValueError("insufficient funds or bad amount")
            self.balances[src] -= amount
            self.balances[dst] += amount
            return {"src": self.balances[src], "dst": self.balances[dst]}

        return self.store.execute(key, {"src": src, "dst": dst, "amount": amount}, effect)
