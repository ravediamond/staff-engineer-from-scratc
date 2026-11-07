"""Review: job completion handler. Eval results were occasionally written twice, and once a slow worker's
stale results overwrote the fresh ones. Find the bug, fix it, explain:

WHY:
"""


class Jobs:
    def __init__(self, clock, lease=60):
        self.clock, self.lease = clock, lease
        self.jobs = {}
        self.next_token = 1

    def take(self, job_id):
        tok = self.next_token
        self.next_token += 1
        self.jobs[job_id] = {"token": tok, "until": self.clock() + self.lease, "done": False}
        return tok

    def complete(self, job_id, token):
        j = self.jobs[job_id]
        if j["done"]:
            return False
        j["done"] = True
        return True
