"""W12 D4: aggregate interview scores the way calibrated loops do."""


def normalize(weights: dict) -> dict:
    """Weights scaled to sum to 1."""
    total = sum(weights.values())
    return {k: v / total for k, v in weights.items()}


def weighted_score(scores: dict, weights: dict) -> float:
    """Sum of normalized weight * score over the axes in weights."""
    w = normalize(weights)
    return sum(w[a] * scores[a] for a in w)


def decision(scores: dict, weights: dict, floors: dict, bar: float = 3.0) -> str:
    """Scores 1-4. If any axis is below its floor -> "lean no" (or "no hire" if it is 1).
    Else by weighted score: >= bar + 0.5 -> "strong hire"; >= bar -> "hire"; >= bar - 0.5 -> "lean no"; else "no hire"."""
    for a, f in floors.items():
        if scores[a] < f:
            return "no hire" if scores[a] == 1 else "lean no"
    s = weighted_score(scores, weights)
    if s >= bar + 0.5:
        return "strong hire"
    if s >= bar:
        return "hire"
    if s >= bar - 0.5:
        return "lean no"
    return "no hire"
