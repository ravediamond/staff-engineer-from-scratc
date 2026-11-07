"""Review: a replay helper. Replayed regression tests pass even when the agent's behaviour clearly changed.
Find the bug, fix it, explain:

WHY:
"""


class Replay:
    def __init__(self, recording):
        self.recording = recording  # list of {"tool", "args", "output"}
        self.used = {}

    def call(self, name, **args):
        for rec in self.recording:
            if rec["tool"] == name:
                return rec["output"]
        raise KeyError(name)
