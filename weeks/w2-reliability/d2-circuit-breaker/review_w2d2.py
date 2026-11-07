"""Review: a breaker that 'worked in staging'. In prod, every time the timer expired, the recovering
service got flattened again. Find the bug, fix it, explain:

WHY:
"""


class Breaker:
    def __init__(self, threshold, reset_timeout, clock, half_open_max=1):
        self.threshold, self.reset_timeout, self.clock = threshold, reset_timeout, clock
        self.half_open_max = half_open_max
        self.state, self.failures, self.opened_at, self.trials = "closed", 0, 0.0, 0

    def allow(self):
        if self.state == "open" and self.clock() - self.opened_at >= self.reset_timeout:
            self.state, self.trials = "half_open", 0
        if self.state == "closed":
            return True
        if self.state == "half_open":
            self.trials += 1
            return True
        return False

    def failure(self):
        self.failures += 1
        if self.state == "half_open" or self.failures >= self.threshold:
            self.state, self.opened_at, self.failures = "open", self.clock(), 0

    def success(self):
        self.failures = 0
        if self.state == "half_open":
            self.state = "closed"
