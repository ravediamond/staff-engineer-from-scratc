"""W5 D4: per-conversation ordering, idempotent sends, monotonic read pointers, presence."""
from collections import defaultdict


class ChatService:
    def __init__(self):
        self.messages: dict = defaultdict(list)    # conv -> [(seq, sender, text)]
        self.by_client_id: dict = {}               # (conv, client_msg_id) -> seq
        self.read: dict = defaultdict(int)         # (user, conv) -> highest seq read

    def send(self, conv, sender, client_msg_id, text) -> int:
        """Assign the next seq for conv (1, 2, 3, ...). Duplicate client_msg_id in the same conv returns
        the original seq without storing again. The sender has implicitly read their own message."""
        key = (conv, client_msg_id)
        if key in self.by_client_id:
            return self.by_client_id[key]
        seq = len(self.messages[conv]) + 1
        self.messages[conv].append((seq, sender, text))
        self.by_client_id[key] = seq
        self.mark_read(sender, conv, seq)
        return seq

    def fetch(self, conv, after_seq: int = 0, limit: int = 50) -> list:
        """Messages with seq > after_seq, ascending, at most limit."""
        return [m for m in self.messages[conv] if m[0] > after_seq][:limit]

    def mark_read(self, user, conv, seq: int) -> None:
        k = (user, conv)
        self.read[k] = max(self.read[k], seq)

    def unread(self, user, conv) -> int:
        return len(self.messages[conv]) - self.read[(user, conv)]


class Presence:
    def __init__(self, timeout: float):
        self.timeout = timeout
        self.last: dict = {}

    def heartbeat(self, user, t: float) -> None:
        self.last[user] = max(self.last.get(user, t), t)

    def is_online(self, user, now: float) -> bool:
        """Online iff a heartbeat arrived within the last `timeout` seconds (now - last < timeout)."""
        t = self.last.get(user)
        return t is not None and now - t < self.timeout

    def online(self, users: list, now: float) -> list:
        return [u for u in users if self.is_online(u, now)]
