"""W10 D3: spans, tool-call recording, deterministic replay with argument checks, trace diff, cost."""
import itertools
from collections import defaultdict


class Tracer:
    def __init__(self, clock):
        self.clock = clock
        self.spans: dict = {}
        self._ids = itertools.count(1)

    def start(self, name: str, parent=None, **attrs) -> int:
        """Create a span {"id", "name", "parent", "attrs", "start", "end": None, "status": None, "output": None}."""
        # TODO
        raise NotImplementedError

    def end(self, span_id: int, status: str = "ok", output=None) -> None:
        # TODO
        raise NotImplementedError

    def children(self, span_id) -> list:
        """Ids of direct children in creation order."""
        # TODO
        raise NotImplementedError

    def duration(self, span_id) -> float:
        # TODO
        raise NotImplementedError


class Recorder:
    """Wraps tools: recorder.call(name, **args) runs the real tool and appends {"tool", "args", "output"}."""

    def __init__(self, tools: dict):
        self.tools = tools
        self.recording: list = []

    def call(self, name: str, **args):
        # TODO
        raise NotImplementedError


class ReplayMismatch(Exception):
    pass


class Replayer:
    """Serves recorded outputs. The k-th call to tool T must have the same args as the k-th recorded call to T;
    otherwise (or if there is no k-th recorded call) raise ReplayMismatch. Never calls a real tool."""

    def __init__(self, recording: list):
        self.by_tool: dict = defaultdict(list)
        for rec in recording:
            self.by_tool[rec["tool"]].append(rec)
        self.counts: dict = defaultdict(int)

    def call(self, name: str, **args):
        # TODO
        raise NotImplementedError


def first_divergence(a: list, b: list):
    """Traces are lists of {"tool", "args", ...}. Index of the first step whose (tool, args) differ, or where one
    trace ends before the other; None if identical in (tool, args)."""
    # TODO
    raise NotImplementedError


def run_cost(spans: dict, usd_per_1k_in: float, usd_per_1k_out: float) -> float:
    """Sum over spans named "model" of attrs["tokens_in"] and attrs["tokens_out"] priced per 1k tokens."""
    # TODO
    raise NotImplementedError
