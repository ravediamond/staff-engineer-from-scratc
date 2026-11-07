"""Self-contained. Run after predict.md."""
import random

random.seed(0)


def merge(iv):
    out = []
    for s, e in sorted(iv):
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


def peak(iv, end_first=True):
    ev = []
    for s, e in iv:
        ev.append((s, 1))
        ev.append((e, -1))
    ev.sort(key=lambda t: (t[0], t[1] if end_first else -t[1]))
    cur = best = 0
    for _, d in ev:
        cur += d
        best = max(best, cur)
    return best


print("1.", merge([[1, 3], [2, 6], [8, 10], [15, 18]]))
m = [(1, 3), (3, 5), (2, 4)]
print("2. half-open peak:", peak(m, end_first=True))
print("3. closed peak:", peak(m, end_first=False))
iv = [(s, s + random.expovariate(1.0)) for s in (random.uniform(0, 1000) for _ in range(1_000_000))]
print("4. mean concurrency = 1000 (arrival rate x mean length); observed peak:", peak(iv), "(Poisson tail: mean + ~4 sigma, sigma = sqrt(1000))")
