"""W4 D4: exact search, k-means, IVF, a greedy k-NN-graph index, recall@k. numpy only. Similarity = cosine."""
import heapq

import numpy as np


def normalize(X: np.ndarray) -> np.ndarray:
    """L2-normalise rows (or a single vector). Zero vectors stay zero."""
    # TODO
    raise NotImplementedError


def exact_topk(X: np.ndarray, q: np.ndarray, k: int) -> np.ndarray:
    """Indices of the k rows most cosine-similar to q, best first."""
    # TODO
    raise NotImplementedError


def kmeans(X: np.ndarray, k: int, iters: int = 10, seed: int = 0) -> np.ndarray:
    """Spherical k-means on normalised X: init = k distinct random rows; assign by max cosine;
    centroid = normalised mean (keep the old centroid if a cell is empty). Return (k, d) centroids."""
    # TODO
    raise NotImplementedError


class IVFIndex:
    def __init__(self, nlist: int, seed: int = 0):
        self.nlist, self.seed = nlist, seed

    def fit(self, X: np.ndarray) -> "IVFIndex":
        """Train centroids, assign each row to its nearest centroid, keep inverted lists of row ids."""
        # TODO
        raise NotImplementedError

    def search(self, q: np.ndarray, k: int, nprobe: int) -> np.ndarray:
        """Scan the nprobe cells whose centroids are most similar to q. Return top-k row ids, best first."""
        # TODO
        raise NotImplementedError


class KNNGraphIndex:
    """Each node linked to its M most similar nodes. Search = greedy best-first with a beam of size ef."""

    def __init__(self, M: int, n_random: int = 4, seed: int = 0):
        self.M, self.n_random, self.seed = M, n_random, seed

    def fit(self, X: np.ndarray) -> "KNNGraphIndex":
        """Links = the M most similar other nodes + n_random random long-range links (rng seeded with seed).
        Without long-range links, a k-NN graph on clustered data splits into islands and greedy search
        from the entry point never leaves the entry's cluster (that is what HNSW's upper layers fix).
        self.nbrs[i] = array of neighbour ids of node i."""
        # TODO
        raise NotImplementedError

    def search(self, q: np.ndarray, k: int, ef: int, entry: int = 0) -> np.ndarray:
        """Best-first search: a max-heap of candidates to expand (by similarity) and a min-heap `best`
        of the top-ef found so far. Stop when the best candidate is worse than the worst of `best`
        and `best` is full. Return the top-k ids of `best`, best first."""
        # TODO
        raise NotImplementedError


def recall_at_k(approx: np.ndarray, exact: np.ndarray, k: int) -> float:
    # TODO
    raise NotImplementedError
