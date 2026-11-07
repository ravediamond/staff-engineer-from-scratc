"""W6 D4: versioned index fed by at-least-once, possibly out-of-order CDC events."""


class VersionedIndex:
    def __init__(self, chunk_size: int = 40):
        self.chunk_size = chunk_size
        self.docs: dict = {}      # doc_id -> {"version": int, "deleted": bool}
        self.chunks: dict = {}    # chunk_id -> {"doc_id", "version", "text"}
        self.applied = 0

    def _chunk(self, text: str) -> list:
        return [text[i:i + self.chunk_size] for i in range(0, len(text), self.chunk_size)] or [""]

    def apply(self, event: dict) -> bool:
        """event: {"op": "upsert"|"delete", "doc_id", "version", "text" (upsert only)}.
        Ignore (return False) if version <= stored version (tombstones included).
        Upsert: remove the doc's old chunks, add chunks with ids f"{doc_id}@{version}#{i}".
        Delete: remove chunks, store a tombstone {"version": v, "deleted": True}.
        Return True if applied (self.applied += 1)."""
        d, v = event["doc_id"], event["version"]
        cur = self.docs.get(d)
        if cur is not None and v <= cur["version"]:
            return False
        for cid in [c for c, ch in self.chunks.items() if ch["doc_id"] == d]:
            del self.chunks[cid]
        if event["op"] == "delete":
            self.docs[d] = {"version": v, "deleted": True}
        else:
            self.docs[d] = {"version": v, "deleted": False}
            for i, piece in enumerate(self._chunk(event["text"])):
                self.chunks[f"{d}@{v}#{i}"] = {"doc_id": d, "version": v, "text": piece}
        self.applied += 1
        return True

    def chunks_for(self, doc_id) -> list:
        """Chunk ids of doc_id, sorted."""
        return sorted(c for c, ch in self.chunks.items() if ch["doc_id"] == doc_id)

    def live_doc_ids(self) -> list:
        return sorted(d for d, s in self.docs.items() if not s["deleted"])

    def search(self, term: str) -> list:
        """Sorted doc ids having a chunk containing term (case-insensitive)."""
        t = term.lower()
        return sorted({ch["doc_id"] for ch in self.chunks.values() if t in ch["text"].lower()})

    def staleness(self, source_versions: dict) -> list:
        """source_versions: doc_id -> current version at the source. Return sorted doc ids where the index
        has no record or an older version."""
        return sorted(d for d, v in source_versions.items() if d not in self.docs or self.docs[d]["version"] < v)
