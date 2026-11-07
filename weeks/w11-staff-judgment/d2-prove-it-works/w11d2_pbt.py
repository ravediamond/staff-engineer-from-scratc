"""W11 D2: a minimal property-based testing framework with greedy shrinking."""
import random


def gen_int(rng: random.Random, lo: int, hi: int) -> int:
    """Uniform in [lo, hi]."""
    return rng.randint(lo, hi)


def gen_list(rng: random.Random, elem_gen, max_len: int) -> list:
    """Length uniform in [0, max_len], elements from elem_gen(rng)."""
    return [elem_gen(rng) for _ in range(rng.randint(0, max_len))]


def shrink_int(x: int) -> list:
    """Candidates in order: 0, x // 2 toward zero (int(x / 2)), x - 1 if x > 0 else x + 1. Exclude x; dedupe, keep order."""
    if x == 0:
        return []
    cands = [0, int(x / 2), x - 1 if x > 0 else x + 1]
    out = []
    for c in cands:
        if c != x and c not in out:
            out.append(c)
    return out


def shrink_list(xs: list, shrink_elem) -> list:
    """Candidates in order: [], first half xs[:len//2], second half xs[len//2:], each element removed (i = 0..),
    then each element replaced by each of its shrink candidates. Exclude candidates equal to xs; dedupe, keep order."""
    if not xs:
        return []
    half = len(xs) // 2
    cands = [[], xs[:half], xs[half:]]
    cands += [xs[:i] + xs[i + 1:] for i in range(len(xs))]
    for i, x in enumerate(xs):
        for s in shrink_elem(x):
            cands.append(xs[:i] + [s] + xs[i + 1:])
    out = []
    for c in cands:
        if c != xs and c not in out:
            out.append(c)
    return out


def minimize(x, fails, shrinker):
    """Greedy: repeatedly move to the first shrink candidate for which fails(candidate) is True. Return the last
    failing value."""
    current = x
    improved = True
    while improved:
        improved = False
        for c in shrinker(current):
            if fails(c):
                current = c
                improved = True
                break
    return current


def check(prop, gen, shrinker, n: int = 200, seed: int = 0):
    """Run prop on n generated inputs (random.Random(seed)). On the first input where prop is False, return the
    minimized counterexample. Return None if all pass."""
    rng = random.Random(seed)
    for _ in range(n):
        x = gen(rng)
        if not prop(x):
            return minimize(x, lambda v: not prop(v), shrinker)
    return None


def dedupe_sorted_buggy(xs: list) -> list:
    """Provided, deliberately wrong: meant to remove duplicates from a sorted list."""
    out = []
    i = 0
    while i < len(xs):
        out.append(xs[i])
        if i + 1 < len(xs) and xs[i + 1] == xs[i]:
            i += 2
        else:
            i += 1
    return out
