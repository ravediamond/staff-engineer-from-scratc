"""d01 Group anagrams.
Given words, group the anagrams together. Return groups sorted: each group sorted, groups sorted by first word.
group_anagrams(["eat","tea","tan","ate","nat","bat"]) == [["ate","eat","tea"],["bat"],["nat","tan"]]"""
from collections import defaultdict


def group_anagrams(words: list) -> list:
    g = defaultdict(list)
    for w in words:
        g["".join(sorted(w))].append(w)
    return sorted(sorted(v) for v in g.values())
