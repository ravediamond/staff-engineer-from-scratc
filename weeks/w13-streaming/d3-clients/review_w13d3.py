"""Review: offset commits in a home-made consumer-group coordinator.

WHY: commit() accepted any commit. The paused consumer had been removed from the group; when it woke up
it committed its old position for a partition that now belonged to another member, moving the offset
backwards. Commits must be fenced: reject them unless they carry the current generation and come from
the partition's current owner.
"""


class Coordinator:
    def __init__(self):
        self.generation = 0
        self.owner: dict[int, str] = {}
        self.committed: dict[int, int] = {}

    def assign(self, owner: dict[int, str]) -> int:
        self.generation += 1
        self.owner = dict(owner)
        return self.generation

    def commit(self, member: str, generation: int, partition: int, offset: int) -> bool:
        if generation != self.generation or self.owner.get(partition) != member:
            return False
        self.committed[partition] = offset
        return True
