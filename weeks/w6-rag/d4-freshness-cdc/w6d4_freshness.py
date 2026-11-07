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
        # TODO
        raise NotImplementedError

    def chunks_for(self, doc_id) -> list:
        """Chunk ids of doc_id, sorted."""
        # TODO
        raise NotImplementedError

    def live_doc_ids(self) -> list:
        # TODO
        raise NotImplementedError

    def search(self, term: str) -> list:
        """Sorted doc ids having a chunk containing term (case-insensitive)."""
        # TODO
        raise NotImplementedError

    def staleness(self, source_versions: dict) -> list:
        """source_versions: doc_id -> current version at the source. Return sorted doc ids where the index
        has no record or an older version."""
        # TODO
        raise NotImplementedError
