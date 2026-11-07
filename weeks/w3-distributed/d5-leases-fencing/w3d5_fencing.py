"""W3 D5: lease-based lock service with fencing tokens, and storage that enforces them."""


class StaleToken(Exception):
    pass


class LockService:
    def __init__(self, lease: float, clock):
        self.lease, self.clock = lease, clock
        self.holder = None
        self.token = 0          # last token issued
        self.expires = 0.0

    def _free(self) -> bool:
        return self.holder is None or self.clock() >= self.expires

    def acquire(self, client: str):
        """Grant if free or expired: new token = previous + 1. Return token, or None if held by someone valid.
        A client re-acquiring its own valid lease gets None (it should renew)."""
        # TODO
        raise NotImplementedError

    def renew(self, client: str, token: int) -> bool:
        """Extend the lease only if client still validly holds it with this token."""
        # TODO
        raise NotImplementedError

    def release(self, client: str, token: int) -> None:
        # TODO
        raise NotImplementedError


class FencedStorage:
    def __init__(self):
        self.data: dict = {}
        self.max_token: dict = {}
        self.accepted: list = []  # (resource, value, token)

    def write(self, resource: str, value, token: int) -> None:
        # TODO
        raise NotImplementedError


def simulate_gc_pause() -> tuple:
    """A acquires at t=0 (lease 10), pauses until t=40. B acquires at t=15 and writes "B".
    A wakes at t=40 and tries to write "A" with its old token (catch StaleToken).
    Return (final value of resource "file", list of accepted writer values in order)."""
    # TODO
    raise NotImplementedError
