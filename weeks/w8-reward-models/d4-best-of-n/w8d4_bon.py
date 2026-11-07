"""W8 D4: best-of-N sampling, its KL, and the reward over-optimisation curve in a toy world."""
import math
import random


def bon_kl(n: int) -> float:
    """KL(best-of-n || base) = log n - (n - 1) / n."""
    # TODO
    raise NotImplementedError


def sample(rng: random.Random) -> tuple:
    """Provided: one response = (quality q ~ N(0,1), length l = |N(0,1)|)."""
    return rng.gauss(0, 1), abs(rng.gauss(0, 1))


def proxy(s: tuple) -> float:
    """The learned RM: likes quality and (wrongly) length. q + 1.5 * l."""
    # TODO
    raise NotImplementedError


def gold(s: tuple) -> float:
    """The true reward: q - 0.3 * l^2."""
    # TODO
    raise NotImplementedError


def best_of_n(samples: list, score_fn):
    """The sample with the highest score_fn (first one on ties)."""
    # TODO
    raise NotImplementedError


def overoptimization_curve(ns: list, trials: int = 500, seed: int = 0) -> list:
    """For each n: draw `trials` independent groups of n samples (one shared random.Random(seed), drawn in
    order n by n, trial by trial), pick best_of_n by PROXY, record mean proxy and mean GOLD of the picks.
    Return [(n, bon_kl(n), mean_proxy, mean_gold)]."""
    # TODO
    raise NotImplementedError


def gold_peak_n(curve: list) -> int:
    """n with the highest mean gold."""
    # TODO
    raise NotImplementedError
