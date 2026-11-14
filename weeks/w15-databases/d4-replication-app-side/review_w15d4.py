"""Review: the read router of a web backend with one primary and async replicas.

WHY: it picked any healthy replica, ignoring replication lag. Right after a write, the replica had not
applied it yet, so the user read their own stale data. Read-your-writes: only use a replica whose applied
LSN has reached the session's last write; otherwise read from the primary.
"""


def pick_node(replicas: dict[str, dict], session_last_write_lsn: int) -> str:
    ok = sorted(name for name, r in replicas.items() if r["healthy"] and r["applied_lsn"] >= session_last_write_lsn)
    return ok[0] if ok else "primary"
