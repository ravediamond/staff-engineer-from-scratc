"""Review: a hand-rolled reduce-scatter for a custom accelerator. All-reduce results are wrong for N > 2.
Find the bug, fix it, explain:

WHY:
"""
import numpy as np


def reduce_scatter(bufs):
    N, L = len(bufs), len(bufs[0])
    size = L // N  # assume L divisible by N
    for s in range(N - 1):
        msgs = []
        for i in range(N):
            c = (i + s) % N
            msgs.append(((i + 1) % N, c, bufs[i][c * size:(c + 1) * size].copy()))
        for dst, c, data in msgs:
            bufs[dst][c * size:(c + 1) * size] += data
    return bufs
