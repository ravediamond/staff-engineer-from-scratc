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
        # TODO
        raise NotImplementedError

    def fetch(self, conv, after_seq: int = 0, limit: int = 50) -> list:
        """Messages with seq > after_seq, ascending, at most limit."""
        # TODO
        raise NotImplementedError

    def mark_read(self, user, conv, seq: int) -> None:
        # TODO
        raise NotImplementedError

    def unread(self, user, conv) -> int:
        # TODO
        raise NotImplementedError


class Presence:
    def __init__(self, timeout: float):
        self.timeout = timeout
        self.last: dict = {}

    def heartbeat(self, user, t: float) -> None:
        # TODO
        raise NotImplementedError

    def is_online(self, user, now: float) -> bool:
        """Online iff a heartbeat arrived within the last `timeout` seconds (now - last < timeout)."""
        # TODO
        raise NotImplementedError

    def online(self, users: list, now: float) -> list:
        # TODO
        raise NotImplementedError
