"""d31 Word break: can s be segmented into words from the dictionary (reuse allowed)?"""


def word_break(s: str, words: list) -> bool:
    ws = set(words)
    lens = {len(w) for w in ws}
    ok = [True] + [False] * len(s)
    for i in range(1, len(s) + 1):
        ok[i] = any(L <= i and ok[i - L] and s[i - L:i] in ws for L in lens)
    return ok[-1]
