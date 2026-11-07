"""W1 D4: trie with counts, deletion with pruning, and top-k autocomplete."""
import heapq


class _Node:
    __slots__ = ("children", "is_word", "count")

    def __init__(self):
        self.children: dict = {}
        self.is_word = False
        self.count = 0


class Trie:
    def __init__(self):
        self.root = _Node()

    def _walk(self, s: str):
        """Node at the end of path s, or None."""
        # TODO
        raise NotImplementedError

    def insert(self, word: str, count: int = 1) -> None:
        # TODO
        raise NotImplementedError

    def contains(self, word: str) -> bool:
        # TODO
        raise NotImplementedError

    def starts_with(self, prefix: str) -> bool:
        # TODO
        raise NotImplementedError

    def delete(self, word: str) -> bool:
        """Remove word. Prune nodes that are no longer on any word's path. False if absent."""
        # TODO
        raise NotImplementedError

    def top_k(self, prefix: str, k: int) -> list:
        """Up to k words starting with prefix, sorted by count desc, then word asc."""
        # TODO
        raise NotImplementedError

    def node_count(self) -> int:
        """Number of nodes including the root."""
        # TODO
        raise NotImplementedError
