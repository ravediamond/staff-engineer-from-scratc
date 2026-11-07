"""Review: the 'BoN quality report' used to justify spending 8x inference on every request.
Users saw no improvement. Find the bug, fix it, explain:

WHY:
"""


def bon_report(groups, rm_score, heldout_judge):
    """groups: list of lists of candidate responses. Pick by rm_score. Return the mean quality of picks."""
    total = 0.0
    for cands in groups:
        pick = max(cands, key=rm_score)
        total += heldout_judge(pick)
    return total / len(groups)
