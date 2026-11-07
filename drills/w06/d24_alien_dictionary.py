"""d24 Alien dictionary: words sorted in an unknown alphabet. Return an order of all letters consistent with it,
or "" if impossible (a cycle, or a word before its own prefix). When several orders are valid, pick the
lexicographically smallest (use a heap in Kahn's algorithm)."""
import heapq


def alien_order(words: list) -> str:
    letters = {c for w in words for c in w}
    adj = {c: set() for c in letters}
    indeg = {c: 0 for c in letters}
    for a, b in zip(words, words[1:]):
        for x, y in zip(a, b):
            if x != y:
                if y not in adj[x]:
                    adj[x].add(y)
                    indeg[y] += 1
                break
        else:
            if len(a) > len(b):
                return ""
    heap = [c for c in letters if indeg[c] == 0]
    heapq.heapify(heap)
    out = []
    while heap:
        c = heapq.heappop(heap)
        out.append(c)
        for d in adj[c]:
            indeg[d] -= 1
            if indeg[d] == 0:
                heapq.heappush(heap, d)
    return "".join(out) if len(out) == len(letters) else ""
