"""Review: high-watermark bookkeeping in a home-made replicated log.

WHY: the HW was set to the leader's own log end on every append, so consumers could read records that
existed only on the leader. When the leader died, the new leader did not have them: consumers had
acted on data that was never committed. HW = min LEO over the ISR (leader included), recomputed when a
follower reports progress.
"""


class Leader:
    def __init__(self, isr: set[str]):
        self.log: list = []
        self.isr = set(isr)
        self.follower_leo = {f: 0 for f in isr}
        self.hw = 0

    def _advance(self) -> None:
        self.hw = max(self.hw, min([len(self.log)] + [self.follower_leo[f] for f in self.isr]))

    def append(self, value) -> int:
        self.log.append(value)
        self._advance()
        return len(self.log) - 1

    def on_fetch(self, follower: str, follower_leo: int) -> None:
        self.follower_leo[follower] = follower_leo
        self._advance()

    def consumer_read(self, offset: int) -> list:
        return self.log[offset:self.hw]
