"""Review: a chunker. Retrieval misses facts that are definitely in the documents.
Find the bug, fix it, explain:

WHY:
"""


def windows(text, size, overlap):
    out, start = [], 0
    while start < len(text):
        out.append((start, min(start + size, len(text))))
        start += size + overlap
    return out
