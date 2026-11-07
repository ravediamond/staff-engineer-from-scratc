"""Review: permission-aware retrieval. Restricted users get empty answers most of the time.
Find the bug, fix it, explain:

WHY:
"""


def search(scores, acl, groups, k):
    allowed = [c for c in scores if acl[c] & groups]
    return sorted(allowed, key=lambda c: -scores[c])[:k]
