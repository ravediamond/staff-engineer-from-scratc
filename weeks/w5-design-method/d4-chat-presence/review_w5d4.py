"""Review: read receipts. On flaky networks, users see unread badges come back for messages they read.
Find the bug, fix it, explain:

WHY:
"""


class Receipts:
    def __init__(self):
        self.pointer = {}

    def ack(self, user, conv, seq):
        self.pointer[(user, conv)] = seq

    def unread(self, user, conv, last_seq):
        return last_seq - self.pointer.get((user, conv), 0)
