"""W9 D1: ring all-reduce in numpy. bufs[i] is worker i's buffer (1-D array, same length for all)."""
import numpy as np


def chunk_bounds(L: int, N: int) -> list:
    """N contiguous (start, end) chunks covering range(L); the first L % N chunks get one extra element."""
    # TODO
    raise NotImplementedError


def reduce_scatter(bufs: list) -> list:
    """In place. N-1 steps; at step s every worker i sends chunk (i - s) % N to worker (i + 1) % N, which adds it.
    All sends of a step use values from BEFORE the step (simultaneous exchange).
    After: worker i holds the full sum in chunk (i + 1) % N. Return elements sent per worker."""
    # TODO
    raise NotImplementedError


def all_gather(bufs: list) -> list:
    """In place, after reduce_scatter. N-1 steps; at step s worker i sends chunk (i + 1 - s) % N to (i + 1) % N,
    which overwrites its copy. Return elements sent per worker."""
    # TODO
    raise NotImplementedError


def ring_allreduce(bufs: list) -> tuple:
    """Copies the inputs, runs reduce_scatter then all_gather. Return (list of result arrays, sent per worker)."""
    # TODO
    raise NotImplementedError


def ring_bytes_per_worker(N: int, size_bytes: float) -> float:
    # TODO
    raise NotImplementedError


def param_server_bytes_at_server(N: int, size_bytes: float) -> float:
    """Bytes the server RECEIVES per step when N workers each push their full gradient (server is not a worker)."""
    # TODO
    raise NotImplementedError
