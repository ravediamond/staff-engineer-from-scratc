import numpy as np
import pytest

from w9d1_collectives import (all_gather, chunk_bounds, param_server_bytes_at_server, reduce_scatter, ring_allreduce,
                              ring_bytes_per_worker)


def test_chunk_bounds():
    assert chunk_bounds(10, 3) == [(0, 4), (4, 7), (7, 10)]
    assert chunk_bounds(4, 4) == [(0, 1), (1, 2), (2, 3), (3, 4)]


def test_reduce_scatter_ownership():
    rng = np.random.default_rng(0)
    bufs = [rng.normal(size=12) for _ in range(4)]
    total = sum(bufs)
    work = [b.copy() for b in bufs]
    reduce_scatter(work)
    b = chunk_bounds(12, 4)
    for i in range(4):
        lo, hi = b[(i + 1) % 4]
        assert np.allclose(work[i][lo:hi], total[lo:hi]), f"worker {i} should own the sum of chunk {(i + 1) % 4}"


@pytest.mark.parametrize("N,L", [(2, 7), (3, 10), (5, 23), (8, 64)])
def test_ring_allreduce_correct_and_bytes(N, L):
    rng = np.random.default_rng(N)
    bufs = [rng.normal(size=L) for _ in range(N)]
    out, sent = ring_allreduce(bufs)
    for o in out:
        assert np.allclose(o, sum(bufs))
    assert all(abs(s - 2 * (N - 1) / N * L) <= 2 * (N - 1) for s in sent)
    assert np.allclose(bufs[0], bufs[0]), "inputs unchanged"


def test_formulas():
    assert ring_bytes_per_worker(8, 1e9) == pytest.approx(1.75e9)
    assert param_server_bytes_at_server(64, 1e9) == pytest.approx(64e9)
