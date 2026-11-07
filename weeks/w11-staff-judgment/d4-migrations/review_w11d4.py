"""Review: migration controller. During the vector-DB migration, reads flipped to the new store while 4% of
documents were missing from it. Find the bug, fix it, explain:

WHY:
"""


class Controller:
    def __init__(self, threshold):
        self.threshold = threshold
        self.reads = "old"
        self.verified_rate = None

    def record_verification(self, mismatch_rate):
        self.verified_rate = mismatch_rate

    def cutover(self):
        if self.verified_rate is not None and self.verified_rate <= self.threshold:
            self.reads = "new"
        return self.reads
