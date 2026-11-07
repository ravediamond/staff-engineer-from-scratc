"""W4 D3: inverted index, BM25 ranking, boolean AND."""
import math
import re
from collections import Counter, defaultdict


def tokenize(text: str) -> list:
    # TODO
    raise NotImplementedError


class InvertedIndex:
    def __init__(self):
        self.postings: dict = defaultdict(dict)  # term -> {doc_id: tf}
        self.doc_len: dict = {}

    def add(self, doc_id, text: str) -> None:
        # TODO
        raise NotImplementedError

    @property
    def n_docs(self) -> int:
        return len(self.doc_len)

    @property
    def avgdl(self) -> float:
        # TODO
        raise NotImplementedError

    def df(self, term: str) -> int:
        # TODO
        raise NotImplementedError

    def idf(self, term: str) -> float:
        # TODO
        raise NotImplementedError

    def bm25(self, query: str, k: int = 10, k1: float = 1.5, b: float = 0.75) -> list:
        """Top-k (doc_id, score), score desc then doc_id asc. Repeated query terms count once."""
        # TODO
        raise NotImplementedError

    def search_and(self, query: str) -> list:
        """Doc ids containing ALL query terms, sorted. Intersect starting from the shortest postings list."""
        # TODO
        raise NotImplementedError
