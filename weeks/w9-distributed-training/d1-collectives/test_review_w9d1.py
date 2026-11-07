import numpy as np

from review_w9d1 import reduce_scatter


def test_review_owner_has_full_sum():
    N, L = 4, 8
    bufs = [np.arange(L, dtype=float) * (i + 1) for i in range(N)]
    total = sum(bufs)
    out = reduce_scatter([b.copy() for b in bufs])
    size = L // N
    for i in range(N):
        c = (i + 1) % N
        assert np.allclose(out[i][c * size:(c + 1) * size], total[c * size:(c + 1) * size])
