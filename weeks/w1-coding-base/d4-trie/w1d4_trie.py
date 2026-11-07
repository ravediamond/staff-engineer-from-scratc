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
        n = self.root
        for ch in s:
            n = n.children.get(ch)
            if n is None:
                return None
        return n

    def insert(self, word: str, count: int = 1) -> None:
        n = self.root
        for ch in word:
            n = n.children.setdefault(ch, _Node())
        n.is_word = True
        n.count += count

    def contains(self, word: str) -> bool:
        n = self._walk(word)
        return n is not None and n.is_word

    def starts_with(self, prefix: str) -> bool:
        return self._walk(prefix) is not None

    def delete(self, word: str) -> bool:
        """Remove word. Prune nodes that are no longer on any word's path. False if absent."""
        path = [self.root]
        for ch in word:
            nxt = path[-1].children.get(ch)
            if nxt is None:
                return False
            path.append(nxt)
        if not path[-1].is_word:
            return False
        path[-1].is_word = False
        path[-1].count = 0
        for i in range(len(word), 0, -1):
            n = path[i]
            if n.is_word or n.children:
                break
            del path[i - 1].children[word[i - 1]]
        return True

    def top_k(self, prefix: str, k: int) -> list:
        """Up to k words starting with prefix, sorted by count desc, then word asc."""
        start = self._walk(prefix)
        if start is None or k <= 0:
            return []
        found = []
        stack = [(start, prefix)]
        while stack:
            n, s = stack.pop()
            if n.is_word:
                found.append((-n.count, s))
            for ch, child in n.children.items():
                stack.append((child, s + ch))
        return [w for _, w in heapq.nsmallest(k, found)]

    def node_count(self) -> int:
        """Number of nodes including the root."""
        total, stack = 0, [self.root]
        while stack:
            n = stack.pop()
            total += 1
            stack.extend(n.children.values())
        return total
