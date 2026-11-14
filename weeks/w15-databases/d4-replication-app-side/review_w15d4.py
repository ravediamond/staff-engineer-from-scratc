"""Review: the read router of a web backend with one primary and async replicas. Support tickets: "I changed my
delivery address, the confirmation page showed the old one, so I changed it again". Find the bug, fix it, explain:

WHY:
"""


def pick_node(replicas: dict[str, dict], session_last_write_lsn: int) -> str:
    """replicas: name -> {"healthy": bool, "applied_lsn": int}. Returns the node to read from."""
    healthy = sorted(name for name, r in replicas.items() if r["healthy"])
    return healthy[0] if healthy else "primary"
