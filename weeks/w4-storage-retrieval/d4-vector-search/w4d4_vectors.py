"""W4 D4: exact search, k-means, IVF, a greedy k-NN-graph index, recall@k. numpy only. Similarity = cosine."""
import heapq

import numpy as np


def normalize(X: np.ndarray) -> np.ndarray:
    """L2-normalise rows (or a single vector). Zero vectors stay zero."""
    n = np.linalg.norm(X, axis=-1, keepdims=True)
    return X / np.where(n == 0, 1, n)


def exact_topk(X: np.ndarray, q: np.ndarray, k: int) -> np.ndarray:
    """Indices of the k rows most cosine-similar to q, best first."""
    sims = normalize(X) @ normalize(q)
    idx = np.argpartition(-sims, min(k, len(sims) - 1))[:k]
    return idx[np.argsort(-sims[idx], kind="stable")]


def kmeans(X: np.ndarray, k: int, iters: int = 10, seed: int = 0) -> np.ndarray:
    """Spherical k-means on normalised X: init = k distinct random rows; assign by max cosine;
    centroid = normalised mean (keep the old centroid if a cell is empty). Return (k, d) centroids."""
    Xn = normalize(X)
    rng = np.random.default_rng(seed)
    C = Xn[rng.choice(len(Xn), k, replace=False)].copy()
    for _ in range(iters):
        a = np.argmax(Xn @ C.T, axis=1)
        for j in range(k):
            m = a == j
            if m.any():
                C[j] = Xn[m].mean(0)
        C = normalize(C)
    return C


class IVFIndex:
    def __init__(self, nlist: int, seed: int = 0):
        self.nlist, self.seed = nlist, seed

    def fit(self, X: np.ndarray) -> "IVFIndex":
        """Train centroids, assign each row to its nearest centroid, keep inverted lists of row ids."""
        self.X = normalize(X)
        self.C = kmeans(self.X, self.nlist, seed=self.seed)
        a = np.argmax(self.X @ self.C.T, axis=1)
        self.lists = [np.where(a == j)[0] for j in range(self.nlist)]
        return self

    def search(self, q: np.ndarray, k: int, nprobe: int) -> np.ndarray:
        """Scan the nprobe cells whose centroids are most similar to q. Return top-k row ids, best first."""
        qn = normalize(q)
        cells = np.argsort(-(self.C @ qn))[:nprobe]
        cand = np.concatenate([self.lists[c] for c in cells])
        if len(cand) == 0:
            return cand
        sims = self.X[cand] @ qn
        order = np.argsort(-sims, kind="stable")[:k]
        return cand[order]


class KNNGraphIndex:
    """Each node linked to its M most similar nodes. Search = greedy best-first with a beam of size ef."""

    def __init__(self, M: int, n_random: int = 4, seed: int = 0):
        self.M, self.n_random, self.seed = M, n_random, seed

    def fit(self, X: np.ndarray) -> "KNNGraphIndex":
        """Links = the M most similar other nodes + n_random random long-range links (rng seeded with seed).
        Without long-range links, a k-NN graph on clustered data splits into islands and greedy search
        from the entry point never leaves the entry's cluster (that is what HNSW's upper layers fix).
        self.nbrs[i] = array of neighbour ids of node i."""
        self.X = normalize(X)
        S = self.X @ self.X.T
        np.fill_diagonal(S, -np.inf)
        near = np.argsort(-S, axis=1)[:, : self.M]
        rng = np.random.default_rng(self.seed)
        far = rng.integers(0, len(X), size=(len(X), self.n_random))
        self.nbrs = np.concatenate([near, far], axis=1)
        return self

    def search(self, q: np.ndarray, k: int, ef: int, entry: int = 0) -> np.ndarray:
        """Best-first search: a max-heap of candidates to expand (by similarity) and a min-heap `best`
        of the top-ef found so far. Stop when the best candidate is worse than the worst of `best`
        and `best` is full. Return the top-k ids of `best`, best first."""
        qn = normalize(q)
        sim = lambda i: float(self.X[i] @ qn)
        visited = {entry}
        s0 = sim(entry)
        cand = [(-s0, entry)]
        best = [(s0, entry)]
        while cand:
            neg_s, node = heapq.heappop(cand)
            if len(best) >= ef and -neg_s < best[0][0]:
                break
            for nb in self.nbrs[node]:
                nb = int(nb)
                if nb in visited:
                    continue
                visited.add(nb)
                s = sim(nb)
                if len(best) < ef or s > best[0][0]:
                    heapq.heappush(cand, (-s, nb))
                    heapq.heappush(best, (s, nb))
                    if len(best) > ef:
                        heapq.heappop(best)
        return np.array([i for _, i in sorted(best, reverse=True)[:k]])


def recall_at_k(approx: np.ndarray, exact: np.ndarray, k: int) -> float:
    return len(set(approx[:k].tolist()) & set(exact[:k].tolist())) / k
