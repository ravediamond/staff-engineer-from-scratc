"""W3 D4: Raft log replication (no elections). Logs are 1-indexed lists of (term, command)."""


class Follower:
    def __init__(self, log=None, current_term: int = 0):
        self.log: list = list(log or [])
        self.current_term = current_term
        self.commit_index = 0

    def term_at(self, index: int) -> int:
        """Term of entry at 1-based index; 0 for index 0; -1 if no such entry."""
        # TODO
        raise NotImplementedError

    def append_entries(self, term: int, prev_index: int, prev_term: int, entries: list,
                       leader_commit: int) -> tuple:
        """Return (success, match_index). match_index = prev_index + len(entries) on success, else 0."""
        # TODO
        raise NotImplementedError


class Leader:
    def __init__(self, log: list, current_term: int, follower_ids: list):
        self.log = list(log)
        self.current_term = current_term
        self.commit_index = 0
        self.next_index = {f: len(log) + 1 for f in follower_ids}
        self.match_index = {f: 0 for f in follower_ids}

    def append(self, command) -> None:
        self.log.append((self.current_term, command))

    def request_for(self, f) -> dict:
        """AppendEntries args for follower f: everything from next_index[f] on."""
        # TODO
        raise NotImplementedError

    def on_response(self, f, success: bool, match_index: int) -> None:
        # TODO
        raise NotImplementedError

    def advance_commit(self) -> int:
        """Highest N > commit_index with a majority (leader counts itself) having match >= N
        AND log[N].term == current_term. Return the new commit_index."""
        # TODO
        raise NotImplementedError


def replicate_until_stable(leader: Leader, followers: dict, reachable=None, max_rounds: int = 50) -> None:
    """Send AppendEntries to every reachable follower until nothing changes, then advance commit."""
    reachable = set(followers) if reachable is None else set(reachable)
    for _ in range(max_rounds):
        changed = False
        for f, node in followers.items():
            if f not in reachable:
                continue
            before = (leader.next_index[f], leader.match_index[f])
            ok, m = node.append_entries(**leader.request_for(f))
            leader.on_response(f, ok, m)
            changed |= before != (leader.next_index[f], leader.match_index[f])
        leader.advance_commit()
        if not changed:
            return
