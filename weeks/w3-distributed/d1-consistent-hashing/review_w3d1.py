"""Review: ring lookup. Crashes in prod with IndexError on about 1% of keys. Find the bug, fix it, explain:

WHY:
"""
import bisect
import hashlib


def h(s):
    return int.from_bytes(hashlib.md5(s.encode()).digest()[:8], "big")


class Ring:
    def __init__(self, nodes, vnodes=50):
        pts = sorted((h(f"{n}#{i}"), n) for n in nodes for i in range(vnodes))
        self.hashes = [p for p, _ in pts]
        self.nodes = [n for _, n in pts]

    def lookup(self, key):
        i = bisect.bisect_left(self.hashes, h(key))
        return self.nodes[i % len(self.nodes)]
