"""W12 D4: aggregate interview scores the way calibrated loops do."""


def normalize(weights: dict) -> dict:
    """Weights scaled to sum to 1."""
    # TODO
    raise NotImplementedError


def weighted_score(scores: dict, weights: dict) -> float:
    """Sum of normalized weight * score over the axes in weights."""
    # TODO
    raise NotImplementedError


def decision(scores: dict, weights: dict, floors: dict, bar: float = 3.0) -> str:
    """Scores 1-4. If any axis is below its floor -> "lean no" (or "no hire" if it is 1).
    Else by weighted score: >= bar + 0.5 -> "strong hire"; >= bar -> "hire"; >= bar - 0.5 -> "lean no"; else "no hire"."""
    # TODO
    raise NotImplementedError
