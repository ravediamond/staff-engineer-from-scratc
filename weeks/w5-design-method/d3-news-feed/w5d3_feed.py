"""W5 D3: hybrid fan-out feed."""
import heapq
from collections import defaultdict


def fanout_writes(follower_counts: dict, threshold: int) -> int:
    """Inbox writes if every author posts once: followers of non-celebrities (count < threshold) only."""
    # TODO
    raise NotImplementedError


class FeedService:
    def __init__(self, celebrity_threshold: int, inbox_cap: int = 800):
        self.threshold, self.cap = celebrity_threshold, inbox_cap
        self.followers: dict = defaultdict(set)
        self.following: dict = defaultdict(set)
        self.inbox: dict = defaultdict(list)    # user -> [(ts, post_id)] newest first
        self.outbox: dict = defaultdict(list)   # author -> [(ts, post_id)] newest first
        self.writes = 0
        self.reads = 0

    def is_celebrity(self, user) -> bool:
        return len(self.followers[user]) >= self.threshold

    def follow(self, a, b) -> None:
        """a follows b. (No backfill of b's old posts into a's inbox.)"""
        # TODO
        raise NotImplementedError

    def post(self, author, post_id, ts) -> None:
        """Prepend to outbox. If author is not a celebrity: prepend to each follower's inbox
        (one write each, self.writes += 1), truncating inboxes to inbox_cap. Timestamps increase over time."""
        # TODO
        raise NotImplementedError

    def feed(self, user, n: int) -> list:
        """Up to n post_ids, newest first: user's inbox + outboxes of followed celebrities + user's own outbox.
        Count one read per list fetched (self.reads). No duplicates. Ties on ts: higher post_id first."""
        # TODO
        raise NotImplementedError
