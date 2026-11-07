import numpy as np

from w4d4_vectors import IVFIndex, KNNGraphIndex, exact_topk, kmeans, normalize, recall_at_k


def data(n=3000, d=24, clusters=30, seed=0):
    rng = np.random.default_rng(seed)
    C = rng.normal(size=(clusters, d))
    X = C[rng.integers(0, clusters, n)] + 0.5 * rng.normal(size=(n, d))
    Q = X[rng.integers(0, n, 60)] + 0.1 * rng.normal(size=(60, d))
    return X, Q


def test_normalize():
    X = np.array([[3.0, 4.0], [0.0, 0.0]])
    assert np.allclose(normalize(X), [[0.6, 0.8], [0, 0]])


def test_exact_is_cosine_not_dot():
    X = np.array([[10.0, 0.0], [0.6, 0.8], [0.0, 1.0]])
    q = np.array([0.0, 1.0])
    assert exact_topk(X, q, 2).tolist() == [2, 1]


def test_kmeans_shapes_and_unit_norm():
    X, _ = data()
    C = kmeans(X, 10, iters=5)
    assert C.shape == (10, X.shape[1])
    assert np.allclose(np.linalg.norm(C, axis=1), 1)


def test_ivf_recall_grows_with_nprobe():
    X, Q = data()
    ivf = IVFIndex(nlist=30).fit(X)
    rec = {}
    for nprobe in (1, 5, 30):
        rec[nprobe] = np.mean([recall_at_k(ivf.search(q, 10, nprobe), exact_topk(X, q, 10), 10) for q in Q])
    assert rec[1] <= rec[5] <= rec[30]
    assert rec[30] == 1.0, "scanning every cell is exact search"
    assert rec[5] > 0.8


def test_graph_search_recall():
    X, Q = data()
    g = KNNGraphIndex(M=16).fit(X)
    r_small = np.mean([recall_at_k(g.search(q, 10, ef=10), exact_topk(X, q, 10), 10) for q in Q])
    r_big = np.mean([recall_at_k(g.search(q, 10, ef=80), exact_topk(X, q, 10), 10) for q in Q])
    assert r_big >= r_small and r_big > 0.9


def test_recall_at_k():
    assert recall_at_k(np.array([1, 2, 3]), np.array([3, 4, 1]), 3) == 2 / 3
