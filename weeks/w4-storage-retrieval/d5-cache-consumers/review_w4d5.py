"""Review: a billing consumer. Finance reports missing invoices after every deploy (deploys kill the process).
Find the bug, fix it, explain:

WHY:
"""


class Killed(Exception):
    pass


def consume(log, state, handle, kill_at=None):
    """state: {"offset": int}. Process messages from state["offset"]. kill_at simulates a SIGKILL
    at that offset, between the two steps."""
    for off in range(state["offset"], len(log)):
        handle(log[off])
        if kill_at == off:
            raise Killed(off)
        state["offset"] = off + 1
