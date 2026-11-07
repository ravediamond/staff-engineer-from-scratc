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
        hit = self.data.get(key)
        if hit is not None and self.clock() < hit[1]:
            return hit[0]
        fut = self.inflight.get(key)
        if fut is not None:
            return await fut
        fut = asyncio.get_running_loop().create_future()
        self.inflight[key] = fut
        self.loads += 1
        try:
            value = await self.loader(key)
        except Exception as e:
            fut.set_exception(e)
            del self.inflight[key]
            fut.exception()  # mark retrieved so asyncio does not warn when nobody else waits
            raise
        self.data[key] = (value, self.clock() + self.ttl)
        fut.set_result(value)
        del self.inflight[key]
        return value


class Crash(Exception):
    pass


class Sink:
    """Effect store. In a real system: one DB transaction that updates `total` AND inserts msg_id."""

    def __init__(self):
        self.total = 0
        self.applied_ids: set = set()

    def apply(self, msg_id: str, amount: int) -> bool:
        """Add amount once per msg_id. Return True if applied, False if it was a duplicate."""
        if msg_id in self.applied_ids:
            return False
        self.total += amount
        self.applied_ids.add(msg_id)
        return True


class Consumer:
    def __init__(self, log: list, sink: Sink):
        self.log = log            # list of (msg_id, amount)
        self.sink = sink
        self.committed = 0        # next offset to process (durable in a real system)

    def run(self, crash_after_effect_at=None) -> None:
        """Process from self.committed to the end: apply the effect, THEN commit offset+1.
        If crash_after_effect_at == offset, raise Crash right after the effect, before committing."""
        for off in range(self.committed, len(self.log)):
            msg_id, amount = self.log[off]
            self.sink.apply(msg_id, amount)
            if crash_after_effect_at == off:
                raise Crash(off)
            self.committed = off + 1
