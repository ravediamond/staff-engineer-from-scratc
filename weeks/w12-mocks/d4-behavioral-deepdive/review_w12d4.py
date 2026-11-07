"""Review: the debrief tool. Candidates interviewed by panels with more axes got systematically higher scores.
Find the bug, fix it, explain:

WHY:
"""


def panel_score(scores, weights):
    total = sum(weights.values())
    return sum(weights[a] * scores[a] for a in weights) / total
