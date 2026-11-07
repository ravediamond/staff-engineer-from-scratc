"""Review: capacity doc helper. The network team says the numbers are 8x too low. Find the bug, fix it, explain:

WHY:
"""


def egress_gbps(peak_qps, avg_response_kb):
    bytes_per_s = peak_qps * avg_response_kb * 1000
    return bytes_per_s * 8 / 1e9
