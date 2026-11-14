"""Review: offset commits in a home-made consumer-group coordinator. After a consumer paused for a long GC,
a partition was reprocessed from an old offset: thousands of duplicate emails. Find the bug, fix it, explain:

WHY:
"""


class Coordinator:
    def __init__(self):
        self.generation = 0
        self.owner: dict[int, str] = {}       # partition -> member
        self.committed: dict[int, int] = {}

    def assign(self, owner: dict[int, str]) -> int:
        self.generation += 1
        self.owner = dict(owner)
        return self.generation

    def commit(self, member: str, generation: int, partition: int, offset: int) -> bool:
        self.committed[partition] = offset
        return True
