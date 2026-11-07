"""W4 D3: inverted index, BM25 ranking, boolean AND."""
import math
import re
from collections import Counter, defaultdict


def tokenize(text: str) -> list:
    return re.findall(r"[a-z0-9]+", text.lower())


class InvertedIndex:
    def __init__(self):
        self.postings: dict = defaultdict(dict)  # term -> {doc_id: tf}
        self.doc_len: dict = {}

    def add(self, doc_id, text: str) -> None:
        toks = tokenize(text)
        self.doc_len[doc_id] = len(toks)
        for term, tf in Counter(toks).items():
            self.postings[term][doc_id] = tf

    @property
    def n_docs(self) -> int:
        return len(self.doc_len)

    @property
    def avgdl(self) -> float:
        return sum(self.doc_len.values()) / max(1, self.n_docs)

    def df(self, term: str) -> int:
        return len(self.postings.get(term, {}))

    def idf(self, term: str) -> float:
        df = self.df(term)
        return math.log((self.n_docs - df + 0.5) / (df + 0.5) + 1)

    def bm25(self, query: str, k: int = 10, k1: float = 1.5, b: float = 0.75) -> list:
        """Top-k (doc_id, score), score desc then doc_id asc. Repeated query terms count once."""
        scores: dict = defaultdict(float)
        avgdl = self.avgdl
        for term in set(tokenize(query)):
            idf = self.idf(term)
            for doc, tf in self.postings.get(term, {}).items():
                norm = k1 * (1 - b + b * self.doc_len[doc] / avgdl)
                scores[doc] += idf * tf * (k1 + 1) / (tf + norm)
        return sorted(scores.items(), key=lambda x: (-x[1], x[0]))[:k]

    def search_and(self, query: str) -> list:
        """Doc ids containing ALL query terms, sorted. Intersect starting from the shortest postings list."""
        terms = set(tokenize(query))
        if not terms:
            return []
        lists = sorted((self.postings.get(t, {}) for t in terms), key=len)
        result = set(lists[0])
        for p in lists[1:]:
            result &= p.keys()
            if not result:
                break
        return sorted(result)
