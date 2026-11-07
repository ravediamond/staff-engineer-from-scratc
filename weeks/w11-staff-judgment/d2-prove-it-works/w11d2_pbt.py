"""W11 D2: a minimal property-based testing framework with greedy shrinking."""
import random


def gen_int(rng: random.Random, lo: int, hi: int) -> int:
    """Uniform in [lo, hi]."""
    # TODO
    raise NotImplementedError


def gen_list(rng: random.Random, elem_gen, max_len: int) -> list:
    """Length uniform in [0, max_len], elements from elem_gen(rng)."""
    # TODO
    raise NotImplementedError


def shrink_int(x: int) -> list:
    """Candidates in order: 0, x // 2 toward zero (int(x / 2)), x - 1 if x > 0 else x + 1. Exclude x; dedupe, keep order."""
    # TODO
    raise NotImplementedError


def shrink_list(xs: list, shrink_elem) -> list:
    """Candidates in order: [], first half xs[:len//2], second half xs[len//2:], each element removed (i = 0..),
    then each element replaced by each of its shrink candidates. Exclude candidates equal to xs; dedupe, keep order."""
    # TODO
    raise NotImplementedError


def minimize(x, fails, shrinker):
    """Greedy: repeatedly move to the first shrink candidate for which fails(candidate) is True. Return the last
    failing value."""
    # TODO
    raise NotImplementedError


def check(prop, gen, shrinker, n: int = 200, seed: int = 0):
    """Run prop on n generated inputs (random.Random(seed)). On the first input where prop is False, return the
    minimized counterexample. Return None if all pass."""
    # TODO
    raise NotImplementedError


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
