"""W9 D1: ring all-reduce in numpy. bufs[i] is worker i's buffer (1-D array, same length for all)."""
import numpy as np


def chunk_bounds(L: int, N: int) -> list:
    """N contiguous (start, end) chunks covering range(L); the first L % N chunks get one extra element."""
    base, extra = divmod(L, N)
    out, s = [], 0
    for i in range(N):
        e = s + base + (1 if i < extra else 0)
        out.append((s, e))
        s = e
    return out


def reduce_scatter(bufs: list) -> list:
    """In place. N-1 steps; at step s every worker i sends chunk (i - s) % N to worker (i + 1) % N, which adds it.
    All sends of a step use values from BEFORE the step (simultaneous exchange).
    After: worker i holds the full sum in chunk (i + 1) % N. Return elements sent per worker."""
    N = len(bufs)
    b = chunk_bounds(len(bufs[0]), N)
    sent = [0] * N
    for s in range(N - 1):
        msgs = []
        for i in range(N):
            c = (i - s) % N
            lo, hi = b[c]
            msgs.append(((i + 1) % N, c, bufs[i][lo:hi].copy()))
            sent[i] += hi - lo
        for dst, c, data in msgs:
            lo, hi = b[c]
            bufs[dst][lo:hi] += data
    return sent


def all_gather(bufs: list) -> list:
    """In place, after reduce_scatter. N-1 steps; at step s worker i sends chunk (i + 1 - s) % N to (i + 1) % N,
    which overwrites its copy. Return elements sent per worker."""
    N = len(bufs)
    b = chunk_bounds(len(bufs[0]), N)
    sent = [0] * N
    for s in range(N - 1):
        msgs = []
        for i in range(N):
            c = (i + 1 - s) % N
            lo, hi = b[c]
            msgs.append(((i + 1) % N, c, bufs[i][lo:hi].copy()))
            sent[i] += hi - lo
        for dst, c, data in msgs:
            lo, hi = b[c]
            bufs[dst][lo:hi] = data
    return sent


def ring_allreduce(bufs: list) -> tuple:
    """Copies the inputs, runs reduce_scatter then all_gather. Return (list of result arrays, sent per worker)."""
    work = [np.array(x, dtype=float, copy=True) for x in bufs]
    s1 = reduce_scatter(work)
    s2 = all_gather(work)
    return work, [a + b for a, b in zip(s1, s2)]


def ring_bytes_per_worker(N: int, size_bytes: float) -> float:
    return 2 * (N - 1) / N * size_bytes


def param_server_bytes_at_server(N: int, size_bytes: float) -> float:
    """Bytes the server RECEIVES per step when N workers each push their full gradient (server is not a worker)."""
    return N * size_bytes
