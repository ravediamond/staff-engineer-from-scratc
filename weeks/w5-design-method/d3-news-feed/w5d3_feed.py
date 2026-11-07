"""W5 D3: hybrid fan-out feed."""
import heapq
from collections import defaultdict


def fanout_writes(follower_counts: dict, threshold: int) -> int:
    """Inbox writes if every author posts once: followers of non-celebrities (count < threshold) only."""
    return sum(c for c in follower_counts.values() if c < threshold)


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
        self.following[a].add(b)
        self.followers[b].add(a)

    def post(self, author, post_id, ts) -> None:
        """Prepend to outbox. If author is not a celebrity: prepend to each follower's inbox
        (one write each, self.writes += 1), truncating inboxes to inbox_cap. Timestamps increase over time."""
        self.outbox[author].insert(0, (ts, post_id))
        if self.is_celebrity(author):
            return
        for f in self.followers[author]:
            box = self.inbox[f]
            box.insert(0, (ts, post_id))
            del box[self.cap:]
            self.writes += 1

    def feed(self, user, n: int) -> list:
        """Up to n post_ids, newest first: user's inbox + outboxes of followed celebrities + user's own outbox.
        Count one read per list fetched (self.reads). No duplicates. Ties on ts: higher post_id first."""
        lists = [self.inbox[user], self.outbox[user]]
        lists += [self.outbox[c] for c in self.following[user] if self.is_celebrity(c)]
        self.reads += len(lists)
        out, seen = [], set()
        for ts, pid in heapq.merge(*lists, reverse=True):
            if pid in seen:
                continue
            seen.add(pid)
            out.append(pid)
            if len(out) == n:
                break
        return out
