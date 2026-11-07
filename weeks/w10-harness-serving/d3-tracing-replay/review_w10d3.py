"""Review: a replay helper. Replayed regression tests pass even when the agent's behaviour clearly changed.
Find the bug, fix it, explain:

WHY:
"""


class Replay:
    def __init__(self, recording):
        self.recording = recording  # list of {"tool", "args", "output"}
        self.used = {}

    def call(self, name, **args):
        k = self.used.get(name, 0)
        matches = [r for r in self.recording if r["tool"] == name]
        if k >= len(matches) or matches[k]["args"] != args:
            raise KeyError(f"{name} #{k} with {args} not recorded")
        self.used[name] = k + 1
        return matches[k]["output"]
