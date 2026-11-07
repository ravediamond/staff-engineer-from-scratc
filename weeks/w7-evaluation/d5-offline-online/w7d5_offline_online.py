"""W7 D5: rank agreement between offline and online metrics, and a pre-registered launch rule."""
import statistics


def kendall_tau(x: list, y: list) -> float:
    """tau-a = (concordant - discordant) / (n(n-1)/2). Tied pairs count as neither."""
    n = len(x)
    c = d = 0
    for i in range(n):
        for j in range(i + 1, n):
            s = (x[i] - x[j]) * (y[i] - y[j])
            if s > 0:
                c += 1
            elif s < 0:
                d += 1
    return (c - d) / (n * (n - 1) / 2)


def average_ranks(x: list) -> list:
    """Ranks starting at 1; ties get the average of the ranks they span."""
    order = sorted(range(len(x)), key=lambda i: x[i])
    ranks = [0.0] * len(x)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and x[order[j + 1]] == x[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def spearman(x: list, y: list) -> float:
    """Pearson correlation of average ranks."""
    return statistics.correlation(average_ranks(x), average_ranks(y))


def sign_agreement(pairs: list) -> float:
    """pairs: [(offline_delta, online_delta)]. Fraction with the same strict sign; pairs with a zero delta excluded."""
    kept = [(a, b) for a, b in pairs if a != 0 and b != 0]
    return sum((a > 0) == (b > 0) for a, b in kept) / len(kept)


def launch_decision(offline_ci: tuple, online_ci: tuple, guardrail_breaches: list) -> str:
    """offline_ci, online_ci: (lo, hi) of the treatment-minus-control delta on the primary metric.
    Rules, in order:
      any guardrail breach              -> "rollback"
      online CI entirely below 0        -> "rollback"
      online CI entirely above 0        -> "ship"
      otherwise                         -> "iterate"
    (offline_ci is recorded for the agreement analysis but never overrides online data.)"""
    if guardrail_breaches:
        return "rollback"
    lo, hi = online_ci
    if hi < 0:
        return "rollback"
    if lo > 0:
        return "ship"
    return "iterate"
