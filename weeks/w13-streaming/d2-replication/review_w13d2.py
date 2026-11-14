"""Review: high-watermark bookkeeping in a home-made replicated log. During a broker failure, consumers
processed payments that no longer exist in the log after failover. Find the bug, fix it, explain:

WHY:
"""


class Leader:
    def __init__(self, isr: set[str]):
        self.log: list = []
        self.isr = set(isr)                       # follower names
        self.follower_leo = {f: 0 for f in isr}
        self.hw = 0

    def append(self, value) -> int:
        self.log.append(value)
        self.hw = len(self.log)
        return len(self.log) - 1

    def on_fetch(self, follower: str, follower_leo: int) -> None:
        self.follower_leo[follower] = follower_leo

    def consumer_read(self, offset: int) -> list:
        return self.log[offset:self.hw]
