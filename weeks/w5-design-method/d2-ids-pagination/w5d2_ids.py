"""W5 D2: base62, Snowflake IDs, opaque cursor pagination."""
import base64
import json

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
WORKER_BITS, SEQ_BITS = 10, 12


def base62_encode(n: int) -> str:
    # TODO
    raise NotImplementedError


def base62_decode(s: str) -> int:
    # TODO
    raise NotImplementedError


class ClockMovedBackwards(Exception):
    pass


class Snowflake:
    def __init__(self, worker_id: int, clock_ms, epoch_ms: int = 0):
        assert 0 <= worker_id < (1 << WORKER_BITS)
        self.worker, self.clock, self.epoch = worker_id, clock_ms, epoch_ms
        self.last_ms = -1
        self.seq = 0

    def next_id(self) -> int:
        """(ms - epoch) << 22 | worker << 12 | seq. Same ms: seq += 1; if seq overflows 4095,
        spin on clock_ms() until it advances. Clock earlier than last_ms: raise ClockMovedBackwards."""
        # TODO
        raise NotImplementedError


def snowflake_decode(id_: int, epoch_ms: int = 0) -> tuple:
    """(ms, worker, seq)."""
    # TODO
    raise NotImplementedError


def encode_cursor(created_at: int, id_: int) -> str:
    """Opaque: URL-safe base64 of JSON {"c": created_at, "i": id}."""
    # TODO
    raise NotImplementedError


def decode_cursor(cursor: str) -> tuple:
    # TODO
    raise NotImplementedError


def paginate(items: list, limit: int, cursor: str | None = None) -> tuple:
    """items: dicts with "created_at" and "id" (unique), in ANY order.
    Order = (created_at desc, id desc). Return (page, next_cursor or None).
    Page = the first `limit` items strictly after the cursor position in that order.
    next_cursor is None when there is nothing after the page."""
    # TODO
    raise NotImplementedError
