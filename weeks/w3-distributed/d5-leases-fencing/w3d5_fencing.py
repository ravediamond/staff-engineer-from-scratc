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
        if not self._free():
            return None
        self.token += 1
        self.holder = client
        self.expires = self.clock() + self.lease
        return self.token

    def renew(self, client: str, token: int) -> bool:
        """Extend the lease only if client still validly holds it with this token."""
        if self.holder == client and self.token == token and not self._free():
            self.expires = self.clock() + self.lease
            return True
        return False

    def release(self, client: str, token: int) -> None:
        if self.holder == client and self.token == token:
            self.holder = None


class FencedStorage:
    def __init__(self):
        self.data: dict = {}
        self.max_token: dict = {}
        self.accepted: list = []  # (resource, value, token)

    def write(self, resource: str, value, token: int) -> None:
        if token < self.max_token.get(resource, 0):
            raise StaleToken(f"{token} < {self.max_token[resource]}")
        self.max_token[resource] = token
        self.data[resource] = value
        self.accepted.append((resource, value, token))


def simulate_gc_pause() -> tuple:
    """A acquires at t=0 (lease 10), pauses until t=40. B acquires at t=15 and writes "B".
    A wakes at t=40 and tries to write "A" with its old token (catch StaleToken).
    Return (final value of resource "file", list of accepted writer values in order)."""
    t = [0.0]
    svc = LockService(lease=10, clock=lambda: t[0])
    st = FencedStorage()
    tok_a = svc.acquire("A")
    t[0] = 15
    tok_b = svc.acquire("B")
    st.write("file", "B", tok_b)
    t[0] = 40
    try:
        st.write("file", "A", tok_a)
    except StaleToken:
        pass
    return st.data["file"], [v for _, v, _ in st.accepted]
