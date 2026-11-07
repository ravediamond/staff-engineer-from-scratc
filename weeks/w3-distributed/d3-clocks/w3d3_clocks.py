"""W3 D3: Lamport clock and vector clocks (dicts, missing entry = 0)."""


class LamportClock:
    def __init__(self):
        self.c = 0

    def tick(self) -> int:
        """Local event. Returns the event's timestamp."""
        self.c += 1
        return self.c

    def send(self) -> int:
        """Sending is an event: tick and return the timestamp to attach to the message."""
        return self.tick()

    def receive(self, ts: int) -> int:
        self.c = max(self.c, ts) + 1
        return self.c


def vc_increment(vc: dict, node: str) -> dict:
    out = dict(vc)
    out[node] = out.get(node, 0) + 1
    return out


def vc_merge(a: dict, b: dict) -> dict:
    """Element-wise max."""
    return {k: max(a.get(k, 0), b.get(k, 0)) for k in a.keys() | b.keys()}


def vc_compare(a: dict, b: dict) -> str:
    """'equal' | 'before' (a happened before b) | 'after' | 'concurrent'."""
    ks = a.keys() | b.keys()
    le = all(a.get(k, 0) <= b.get(k, 0) for k in ks)
    ge = all(a.get(k, 0) >= b.get(k, 0) for k in ks)
    if le and ge:
        return "equal"
    if le:
        return "before"
    if ge:
        return "after"
    return "concurrent"


def siblings(versions: list) -> list:
    """versions: [(vc, value)]. Keep those not strictly before any other. Keep one of each equal clock.
    Preserve input order among survivors."""
    out = []
    for i, (vc, val) in enumerate(versions):
        dominated = any(vc_compare(vc, other) == "before" for j, (other, _) in enumerate(versions) if j != i)
        duplicate = any(vc_compare(vc, kept) == "equal" for kept, _ in out)
        if not dominated and not duplicate:
            out.append((vc, val))
    return out
