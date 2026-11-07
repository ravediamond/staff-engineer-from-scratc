"""Review: permission-aware retrieval. Restricted users get empty answers most of the time.
Find the bug, fix it, explain:

WHY:
"""


def search(scores, acl, groups, k):
    top = sorted(scores, key=lambda c: -scores[c])[:k]
    return [c for c in top if acl[c] & groups]
