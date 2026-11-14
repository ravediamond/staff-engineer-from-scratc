"""Review: a hand-written controller that keeps `replicas` workers alive. After an API-server hiccup (the watch
reconnected and replayed recent events), the team found 9 workers running for replicas=6 and a doubled GPU
bill. Find the bug, fix it, explain:

WHY:
"""


class Controller:
    def __init__(self, replicas: int):
        self.replicas = replicas
        self.workers: set[str] = set()
        self.counter = 0

    def _start(self) -> None:
        self.counter += 1
        self.workers.add(f"worker-{self.counter}")

    def start(self) -> None:
        for _ in range(self.replicas):
            self._start()

    def on_event(self, event: tuple[str, str]) -> None:
        """event: ("DELETED", worker_name), delivered at least once."""
        kind, name = event
        if kind == "DELETED":
            self.workers.discard(name)
            self._start()
