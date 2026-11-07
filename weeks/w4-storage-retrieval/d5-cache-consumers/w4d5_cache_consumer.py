"""W4 D5: single-flight cache-aside (asyncio) and an exactly-once-effect consumer."""
import asyncio


class SingleFlightCache:
    def __init__(self, loader, ttl: float, clock):
        self.loader = loader              # async def loader(key) -> value
        self.ttl, self.clock = ttl, clock
        self.data: dict = {}              # key -> (value, expires_at)
        self.inflight: dict = {}          # key -> asyncio.Future
        self.loads = 0

    async def get(self, key):
        """Fresh cached value, or await the in-flight load for key, or start one (and cache the result).
        If the load raises, every waiter gets the exception and nothing is cached."""
        # TODO
        raise NotImplementedError


class Crash(Exception):
    pass


class Sink:
    """Effect store. In a real system: one DB transaction that updates `total` AND inserts msg_id."""

    def __init__(self):
        self.total = 0
        self.applied_ids: set = set()

    def apply(self, msg_id: str, amount: int) -> bool:
        """Add amount once per msg_id. Return True if applied, False if it was a duplicate."""
        # TODO
        raise NotImplementedError


class Consumer:
    def __init__(self, log: list, sink: Sink):
        self.log = log            # list of (msg_id, amount)
        self.sink = sink
        self.committed = 0        # next offset to process (durable in a real system)

    def run(self, crash_after_effect_at=None) -> None:
        """Process from self.committed to the end: apply the effect, THEN commit offset+1.
        If crash_after_effect_at == offset, raise Crash right after the effect, before committing."""
        # TODO
        raise NotImplementedError
