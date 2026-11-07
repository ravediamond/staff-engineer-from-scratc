"""W3 D4: Raft log replication (no elections). Logs are 1-indexed lists of (term, command)."""


class Follower:
    def __init__(self, log=None, current_term: int = 0):
        self.log: list = list(log or [])
        self.current_term = current_term
        self.commit_index = 0

    def term_at(self, index: int) -> int:
        """Term of entry at 1-based index; 0 for index 0; -1 if no such entry."""
        if index == 0:
            return 0
        if index > len(self.log):
            return -1
        return self.log[index - 1][0]

    def append_entries(self, term: int, prev_index: int, prev_term: int, entries: list,
                       leader_commit: int) -> tuple:
        """Return (success, match_index). match_index = prev_index + len(entries) on success, else 0."""
        if term < self.current_term:
            return False, 0
        self.current_term = term
        if self.term_at(prev_index) != prev_term:
            return False, 0
        idx = prev_index
        for t, cmd in entries:
            idx += 1
            existing = self.term_at(idx)
            if existing == -1:
                self.log.append((t, cmd))
            elif existing != t:
                del self.log[idx - 1:]
                self.log.append((t, cmd))
        last_new = prev_index + len(entries)
        if leader_commit > self.commit_index:
            self.commit_index = min(leader_commit, last_new)
        return True, last_new


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
        ni = self.next_index[f]
        prev = ni - 1
        return {
            "term": self.current_term,
            "prev_index": prev,
            "prev_term": self.log[prev - 1][0] if prev > 0 else 0,
            "entries": self.log[ni - 1:],
            "leader_commit": self.commit_index,
        }

    def on_response(self, f, success: bool, match_index: int) -> None:
        if success:
            self.match_index[f] = max(self.match_index[f], match_index)
            self.next_index[f] = self.match_index[f] + 1
        else:
            self.next_index[f] = max(1, self.next_index[f] - 1)

    def advance_commit(self) -> int:
        """Highest N > commit_index with a majority (leader counts itself) having match >= N
        AND log[N].term == current_term. Return the new commit_index."""
        cluster = len(self.match_index) + 1
        for n in range(len(self.log), self.commit_index, -1):
            if self.log[n - 1][0] != self.current_term:
                continue
            votes = 1 + sum(1 for m in self.match_index.values() if m >= n)
            if votes * 2 > cluster:
                self.commit_index = n
                break
        return self.commit_index


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
