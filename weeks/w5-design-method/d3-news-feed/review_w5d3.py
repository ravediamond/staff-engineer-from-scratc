"""Review: the feed merge. Users complain their feed starts with posts from last year. Find the bug, fix it, explain:

WHY:
"""
import heapq


def merge_feeds(lists_newest_first, n):
    """Each list: [(ts, post_id)] sorted newest first. Return the n newest post ids."""
    merged = heapq.merge(*lists_newest_first, reverse=True)
    return [pid for _, pid in merged][:n]
