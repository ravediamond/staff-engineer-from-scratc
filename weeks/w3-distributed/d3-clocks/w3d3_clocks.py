"""W3 D3: Lamport clock and vector clocks (dicts, missing entry = 0)."""


class LamportClock:
    def __init__(self):
        self.c = 0

    def tick(self) -> int:
        """Local event. Returns the event's timestamp."""
        # TODO
        raise NotImplementedError

    def send(self) -> int:
        """Sending is an event: tick and return the timestamp to attach to the message."""
        # TODO
        raise NotImplementedError

    def receive(self, ts: int) -> int:
        # TODO
        raise NotImplementedError


def vc_increment(vc: dict, node: str) -> dict:
    # TODO
    raise NotImplementedError


def vc_merge(a: dict, b: dict) -> dict:
    """Element-wise max."""
    # TODO
    raise NotImplementedError


def vc_compare(a: dict, b: dict) -> str:
    """'equal' | 'before' (a happened before b) | 'after' | 'concurrent'."""
    # TODO
    raise NotImplementedError


def siblings(versions: list) -> list:
    """versions: [(vc, value)]. Keep those not strictly before any other. Keep one of each equal clock.
    Preserve input order among survivors."""
    # TODO
    raise NotImplementedError
