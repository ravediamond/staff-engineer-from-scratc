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
        sid = next(self._ids)
        self.spans[sid] = {"id": sid, "name": name, "parent": parent, "attrs": attrs, "start": self.clock(),
                           "end": None, "status": None, "output": None}
        return sid

    def end(self, span_id: int, status: str = "ok", output=None) -> None:
        s = self.spans[span_id]
        s.update(end=self.clock(), status=status, output=output)

    def children(self, span_id) -> list:
        """Ids of direct children in creation order."""
        return [sid for sid, s in self.spans.items() if s["parent"] == span_id]

    def duration(self, span_id) -> float:
        s = self.spans[span_id]
        return s["end"] - s["start"]


class Recorder:
    """Wraps tools: recorder.call(name, **args) runs the real tool and appends {"tool", "args", "output"}."""

    def __init__(self, tools: dict):
        self.tools = tools
        self.recording: list = []

    def call(self, name: str, **args):
        out = self.tools[name](**args)
        self.recording.append({"tool": name, "args": args, "output": out})
        return out


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
        k = self.counts[name]
        recs = self.by_tool.get(name, [])
        if k >= len(recs):
            raise ReplayMismatch(f"{name} call #{k} was not recorded")
        if recs[k]["args"] != args:
            raise ReplayMismatch(f"{name} call #{k}: args {args} != recorded {recs[k]['args']}")
        self.counts[name] += 1
        return recs[k]["output"]


def first_divergence(a: list, b: list):
    """Traces are lists of {"tool", "args", ...}. Index of the first step whose (tool, args) differ, or where one
    trace ends before the other; None if identical in (tool, args)."""
    for i, (x, y) in enumerate(zip(a, b)):
        if (x["tool"], x["args"]) != (y["tool"], y["args"]):
            return i
    return None if len(a) == len(b) else min(len(a), len(b))


def run_cost(spans: dict, usd_per_1k_in: float, usd_per_1k_out: float) -> float:
    """Sum over spans named "model" of attrs["tokens_in"] and attrs["tokens_out"] priced per 1k tokens."""
    tin = sum(s["attrs"].get("tokens_in", 0) for s in spans.values() if s["name"] == "model")
    tout = sum(s["attrs"].get("tokens_out", 0) for s in spans.values() if s["name"] == "model")
    return tin / 1000 * usd_per_1k_in + tout / 1000 * usd_per_1k_out
