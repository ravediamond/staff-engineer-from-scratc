"""Review: a hand-written controller that keeps `replicas` workers alive.

WHY: it was edge-triggered: "one DELETED event = start one worker". Watch events are delivered at least
once (reconnects replay them), so each replayed event started an extra worker. A controller must be
level-triggered: treat the event as a hint, then compare the observed state with the desired count and
create or delete the difference. Running it twice changes nothing.
"""


class Controller:
    def __init__(self, replicas: int):
        self.replicas = replicas
        self.workers: set[str] = set()
        self.counter = 0

    def _start(self) -> None:
        self.counter += 1
        self.workers.add(f"worker-{self.counter}")

    def reconcile(self) -> None:
        while len(self.workers) < self.replicas:
            self._start()

    def start(self) -> None:
        self.reconcile()

    def on_event(self, event: tuple[str, str]) -> None:
        kind, name = event
        if kind == "DELETED":
            self.workers.discard(name)
        self.reconcile()
