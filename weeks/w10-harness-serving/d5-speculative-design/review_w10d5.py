"""Review: speculative decoding verifier. Outputs got noticeably 'dumber' after enabling it, though it should be
lossless. Find the bug, fix it, explain:

WHY:
"""


def accept_prob(p_x, q_x):
    """Probability of accepting a drafted token with target prob p_x and draft prob q_x."""
    return min(1.0, p_x / q_x)
