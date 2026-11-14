"""W14 D1: a toy API server, a deduplicating work queue, and a level-triggered ReplicaSet controller."""
from collections import deque


class Store:
    """Provided: a toy API server. Objects are dicts keyed by (kind, name)."""

    def __init__(self):
        self.objects: dict[tuple[str, str], dict] = {}
        self.version = 0
        self.events: list[tuple[str, str, str]] = []     # (ADDED | MODIFIED | DELETED, kind, name)

    def _bump(self, what: str, kind: str, name: str) -> None:
        self.version += 1
        self.events.append((what, kind, name))

    def create(self, kind: str, name: str, **fields) -> dict:
        assert (kind, name) not in self.objects, f"{kind}/{name} already exists"
        self._bump("ADDED", kind, name)
        obj = {"kind": kind, "name": name, "created": self.version, **fields}
        self.objects[(kind, name)] = obj
        return obj

    def get(self, kind: str, name: str):
        return self.objects.get((kind, name))

    def list(self, kind: str) -> list[dict]:
        return [o for (k, _), o in sorted(self.objects.items()) if k == kind]

    def update(self, kind: str, name: str, **fields) -> None:
        self.objects[(kind, name)].update(fields)
        self._bump("MODIFIED", kind, name)

    def delete(self, kind: str, name: str) -> None:
        del self.objects[(kind, name)]
        self._bump("DELETED", kind, name)


class WorkQueue:
    """FIFO of keys. A key already waiting is not added again."""

    def __init__(self):
        self._queue: deque = deque()
        self._waiting: set = set()

    def add(self, key) -> None:
        if key not in self._waiting:
            self._waiting.add(key)
            self._queue.append(key)

    def get(self):
        """Pop the oldest key (None if empty). Once popped, the key may be added again."""
        if not self._queue:
            return None
        key = self._queue.popleft()
        self._waiting.discard(key)
        return key

    def __len__(self) -> int:
        return len(self._queue)


def reconcile_replicaset(store: Store, name: str) -> dict:
    """Make the Pods owned by ReplicaSet `name` match its spec. Return {"created": [...], "deleted": [...]}
    (pod names).

    - Owned pods: store.list("Pod") with pod["owner"] == name.
    - ReplicaSet missing (it was deleted): delete every owned pod (garbage collection).
    - Too few: create the missing ones with
        store.create("Pod", f"{name}-{store.version + 1}", owner=name, ready=False)
      (store.version + 1 is unique because every create bumps the version).
    - Too many: delete the surplus, choosing not-ready pods first, then the newest (largest "created").
    - Read the state from the store on every call: no memory between calls, no use of store.events."""
    rs = store.get("ReplicaSet", name)
    pods = [p for p in store.list("Pod") if p["owner"] == name]
    created, deleted = [], []
    want = rs["replicas"] if rs is not None else 0
    if len(pods) < want:
        for _ in range(want - len(pods)):
            pod = store.create("Pod", f"{name}-{store.version + 1}", owner=name, ready=False)
            created.append(pod["name"])
    elif len(pods) > want:
        victims = sorted(pods, key=lambda p: (p["ready"], -p["created"]))[:len(pods) - want]
        for p in victims:
            store.delete("Pod", p["name"])
            deleted.append(p["name"])
    return {"created": created, "deleted": deleted}
