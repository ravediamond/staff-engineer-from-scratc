"""Review: a token bucket from a PR. Load test passed. Next morning, overnight-idle clients sent huge bursts.
Find the bug, fix it, explain:

WHY:
"""


class Bucket:
    def __init__(self, rate, capacity, clock):
        self.rate, self.capacity, self.clock = rate, capacity, clock
        self.tokens, self.last = capacity, clock()

    def allow(self):
        now = self.clock()
        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
