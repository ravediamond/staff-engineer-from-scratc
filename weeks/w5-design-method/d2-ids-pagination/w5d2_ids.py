"""W5 D2: base62, Snowflake IDs, opaque cursor pagination."""
import base64
import json

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
WORKER_BITS, SEQ_BITS = 10, 12


def base62_encode(n: int) -> str:
    if n == 0:
        return ALPHABET[0]
    out = []
    while n:
        n, r = divmod(n, 62)
        out.append(ALPHABET[r])
    return "".join(reversed(out))


def base62_decode(s: str) -> int:
    n = 0
    for ch in s:
        n = n * 62 + ALPHABET.index(ch)
    return n


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
        now = self.clock()
        if now < self.last_ms:
            raise ClockMovedBackwards(f"{now} < {self.last_ms}")
        if now == self.last_ms:
            self.seq = (self.seq + 1) & ((1 << SEQ_BITS) - 1)
            if self.seq == 0:
                while now <= self.last_ms:
                    now = self.clock()
        else:
            self.seq = 0
        self.last_ms = now
        return ((now - self.epoch) << (WORKER_BITS + SEQ_BITS)) | (self.worker << SEQ_BITS) | self.seq


def snowflake_decode(id_: int, epoch_ms: int = 0) -> tuple:
    """(ms, worker, seq)."""
    seq = id_ & ((1 << SEQ_BITS) - 1)
    worker = (id_ >> SEQ_BITS) & ((1 << WORKER_BITS) - 1)
    ms = (id_ >> (WORKER_BITS + SEQ_BITS)) + epoch_ms
    return ms, worker, seq


def encode_cursor(created_at: int, id_: int) -> str:
    """Opaque: URL-safe base64 of JSON {"c": created_at, "i": id}."""
    return base64.urlsafe_b64encode(json.dumps({"c": created_at, "i": id_}).encode()).decode()


def decode_cursor(cursor: str) -> tuple:
    d = json.loads(base64.urlsafe_b64decode(cursor.encode()))
    return d["c"], d["i"]


def paginate(items: list, limit: int, cursor: str | None = None) -> tuple:
    """items: dicts with "created_at" and "id" (unique), in ANY order.
    Order = (created_at desc, id desc). Return (page, next_cursor or None).
    Page = the first `limit` items strictly after the cursor position in that order.
    next_cursor is None when there is nothing after the page."""
    ordered = sorted(items, key=lambda x: (x["created_at"], x["id"]), reverse=True)
    if cursor is not None:
        c, i = decode_cursor(cursor)
        ordered = [x for x in ordered if (x["created_at"], x["id"]) < (c, i)]
    page = ordered[:limit]
    nxt = encode_cursor(page[-1]["created_at"], page[-1]["id"]) if len(ordered) > limit else None
    return page, nxt
