"""Review: a minimal trie. A user reports that searching "car" says not found after inserting "cart" then "car".
Find the bug, fix it, explain:

WHY:
"""


class Trie:
    def __init__(self):
        self.root = {}

    def insert(self, word):
        node = self.root
        for i, ch in enumerate(word):
            if ch not in node:
                node[ch] = {}
            node = node[ch]
        node["$"] = True

    def contains(self, word):
        node = self.root
        for ch in word:
            if ch not in node:
                return False
            node = node[ch]
        return "$" in node
