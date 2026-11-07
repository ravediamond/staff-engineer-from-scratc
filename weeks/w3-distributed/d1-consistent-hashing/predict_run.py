"""Self-contained. Run after predict.md."""
import bisect
import hashlib
from collections import Counter


def h(s):
    return int.from_bytes(hashlib.md5(s.encode()).digest()[:8], "big")


keys = [f"user:{i}" for i in range(100_000)]
a = {k: h(k) % 10 for k in keys}
b = {k: h(k) % 11 for k in keys}
print(f"1. mod N, 10 -> 11: {sum(a[k] != b[k] for k in keys) / len(keys):.1%} moved")


def ring_assign(nodes, v):
    pts = sorted((h(f"{n}#{i}"), n) for n in nodes for i in range(v))
    hs = [p for p, _ in pts]
    return {k: pts[bisect.bisect_left(hs, h(k)) % len(pts)][1] for k in keys}


for v in (1, 200):
    c = Counter(ring_assign([f"n{i}" for i in range(10)], v).values())
    print(f"{2 if v == 1 else 3}. vnodes={v}: max/mean = {max(c.values()) / (len(keys) / 10):.2f}")
r10 = ring_assign([f"n{i}" for i in range(10)], 200)
r11 = ring_assign([f"n{i}" for i in range(11)], 200)
print(f"4. ring 10 -> 11: {sum(r10[k] != r11[k] for k in keys) / len(keys):.1%} moved (ideal 1/11 = 9.1%)")
