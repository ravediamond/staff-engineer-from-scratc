"""W6 D2: hashed dense embeddings, RRF, min-max score fusion, and a hybrid index."""
import hashlib
import math
import re
from collections import Counter, defaultdict

import numpy as np


def tokenize(text: str) -> list:
    return re.findall(r"[a-z0-9]+", text.lower())


class BM25:
    """Provided (you built it in W4 D3)."""

    def __init__(self, docs: dict, k1=1.5, b=0.75):
        self.k1, self.b = k1, b
        self.tf = {d: Counter(tokenize(t)) for d, t in docs.items()}
        self.len = {d: sum(c.values()) for d, c in self.tf.items()}
        self.avgdl = sum(self.len.values()) / len(self.len)
        self.df = Counter(t for c in self.tf.values() for t in c)
        self.n = len(docs)

    def scores(self, query: str) -> dict:
        out = defaultdict(float)
        for t in set(tokenize(query)):
            if t not in self.df:
                continue
            idf = math.log((self.n - self.df[t] + 0.5) / (self.df[t] + 0.5) + 1)
            for d, c in self.tf.items():
                if t in c:
                    norm = self.k1 * (1 - self.b + self.b * self.len[d] / self.avgdl)
                    out[d] += idf * c[t] * (self.k1 + 1) / (c[t] + norm)
        return dict(out)


def hash_embed(text: str, dim: int = 512) -> np.ndarray:
    """Feature hashing of unigrams and bigrams ("a b"). For each feature f:
    h = int of the first 8 bytes of sha256(f) (big-endian); index = h % dim; sign = +1 if (h >> 63) & 1 == 0 else -1.
    Add sign at index. L2-normalise (zero vector stays zero)."""
    # TODO
    raise NotImplementedError


def rrf(rankings: list, k: int = 60) -> list:
    """rankings: lists of doc ids, best first. Return doc ids sorted by RRF score desc, ties by id asc."""
    # TODO
    raise NotImplementedError


def minmax_fuse(score_dicts: list, weights: list) -> dict:
    """Min-max normalise each dict to [0, 1] (all-equal scores -> 1.0), then weighted sum.
    A doc missing from a dict contributes 0 for that dict."""
    # TODO
    raise NotImplementedError


class HybridIndex:
    def __init__(self, docs: dict, dim: int = 512):
        self.ids = list(docs)
        self.bm25 = BM25(docs)
        self.E = np.stack([hash_embed(docs[d], dim) for d in self.ids])
        self.dim = dim

    def dense_scores(self, query: str) -> dict:
        # TODO
        raise NotImplementedError

    def search(self, query: str, k: int = 5, mode: str = "rrf", depth: int = 50) -> list:
        """mode 'bm25' | 'dense': sort that channel's scores desc (ties by id). 'rrf': fuse the top-`depth`
        of both channels with rrf(). Return top-k ids."""
        # TODO
        raise NotImplementedError
