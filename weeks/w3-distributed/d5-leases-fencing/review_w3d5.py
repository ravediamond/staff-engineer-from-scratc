"""Review: fenced storage. It rejects stale writes in the unit test, but after a failover an old writer
corrupted data anyway. Find the bug, fix it, explain:

WHY:
"""


class Stale(Exception):
    pass


class Storage:
    def __init__(self):
        self.value = None
        self.highest = 0

    def write(self, value, token):
        if token < self.highest:
            raise Stale(token)
        self.highest = token
        self.value = value
