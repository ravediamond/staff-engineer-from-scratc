"""W3 D2: leaderless quorum replication with LWW versions and read repair."""


class QuorumError(Exception):
    pass


def overlaps(n: int, r: int, w: int) -> bool:
    return r + w > n


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
        targets = self.up() if targets is None else [t for t in targets if t not in self.down]
        acks = 0
        for t in targets:
            cur = self.data[t].get(key)
            if cur is None or version > cur[0]:
                self.data[t][key] = (version, value)
            acks += 1
        if acks < self.w:
            raise QuorumError(f"{acks} acks < W={self.w}")
        return acks

    def get(self, key, sources=None):
        """Read from sources (default: first r up replicas). Need at least r up sources.
        Return the value with the highest version (None if no replica has the key).
        Read repair: write the winning (version, value) to every source that was stale or missing,
        incrementing self.repairs once per repaired replica."""
        if sources is None:
            sources = self.up()[: self.r]
        else:
            sources = [s for s in sources if s not in self.down]
        if len(sources) < self.r:
            raise QuorumError(f"{len(sources)} sources < R={self.r}")
        responses = {s: self.data[s].get(key) for s in sources}
        present = [v for v in responses.values() if v is not None]
        if not present:
            return None
        best = max(present, key=lambda vv: vv[0])
        for s, v in responses.items():
            if v is None or v[0] < best[0]:
                self.data[s][key] = best
                self.repairs += 1
        return best[1]
