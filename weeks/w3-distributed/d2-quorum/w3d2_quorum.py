"""W3 D2: leaderless quorum replication with LWW versions and read repair."""


class QuorumError(Exception):
    pass


def overlaps(n: int, r: int, w: int) -> bool:
    # TODO
    raise NotImplementedError


class Cluster:
    def __init__(self, n: int, r: int, w: int):
        self.n, self.r, self.w = n, r, w
        self.data = [dict() for _ in range(n)]  # replica -> {key: (version, value)}
        self.down: set = set()
        self.repairs = 0

    def up(self) -> list:
        return [i for i in range(self.n) if i not in self.down]

    def put(self, key, value, version, targets=None) -> int:
        """Write (version, value) to every UP replica in targets (default: all up), keeping the higher
        version if a replica already has one. Return acks. Raise QuorumError if acks < w
        (the partial writes stay: that is how real systems behave)."""
        # TODO
        raise NotImplementedError

    def get(self, key, sources=None):
        """Read from sources (default: first r up replicas). Need at least r up sources.
        Return the value with the highest version (None if no replica has the key).
        Read repair: write the winning (version, value) to every source that was stale or missing,
        incrementing self.repairs once per repaired replica."""
        # TODO
        raise NotImplementedError
