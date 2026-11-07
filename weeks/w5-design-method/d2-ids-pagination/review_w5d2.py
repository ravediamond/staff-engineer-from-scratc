"""Review: an ID generator. Two workers generated the same ID in production. Find the bug, fix it, explain:

WHY:
"""


def make_id(ms, worker, seq):
    """64-bit layout: 41 bits ms | 10 bits worker | 12 bits seq."""
    assert 0 <= worker < 1024 and 0 <= seq < 4096
    return (ms << 22) | (worker << 10) | seq
