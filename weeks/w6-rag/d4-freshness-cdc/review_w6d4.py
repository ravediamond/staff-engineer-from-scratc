"""Review: index updater. After a backfill job ran alongside the live CDC stream, the index served
outdated procedures. Find the bug, fix it, explain:

WHY:
"""


class Index:
    def __init__(self):
        self.docs = {}  # doc_id -> (version, text)

    def upsert(self, doc_id, version, text):
        self.docs[doc_id] = (version, text)
