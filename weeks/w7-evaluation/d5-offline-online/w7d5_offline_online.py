"""W7 D5: rank agreement between offline and online metrics, and a pre-registered launch rule."""
import statistics


def kendall_tau(x: list, y: list) -> float:
    """tau-a = (concordant - discordant) / (n(n-1)/2). Tied pairs count as neither."""
    # TODO
    raise NotImplementedError


def average_ranks(x: list) -> list:
    """Ranks starting at 1; ties get the average of the ranks they span."""
    # TODO
    raise NotImplementedError


def spearman(x: list, y: list) -> float:
    """Pearson correlation of average ranks."""
    # TODO
    raise NotImplementedError


def sign_agreement(pairs: list) -> float:
    """pairs: [(offline_delta, online_delta)]. Fraction with the same strict sign; pairs with a zero delta excluded."""
    # TODO
    raise NotImplementedError


def launch_decision(offline_ci: tuple, online_ci: tuple, guardrail_breaches: list) -> str:
    """offline_ci, online_ci: (lo, hi) of the treatment-minus-control delta on the primary metric.
    Rules, in order:
      any guardrail breach              -> "rollback"
      online CI entirely below 0        -> "rollback"
      online CI entirely above 0        -> "ship"
      otherwise                         -> "iterate"
    (offline_ci is recorded for the agreement analysis but never overrides online data.)"""
    # TODO
    raise NotImplementedError
