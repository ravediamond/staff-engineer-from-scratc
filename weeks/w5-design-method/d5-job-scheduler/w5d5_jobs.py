"""W5 D5: job queue with priorities, delayed jobs, leases with tokens, retries and a dead-letter queue."""
import heapq
import itertools


class JobQueue:
    def __init__(self, lease_seconds: float, max_attempts: int, clock):
        self.lease_seconds, self.max_attempts, self.clock = lease_seconds, max_attempts, clock
        self.ready: list = []           # heap of (-priority, submit_order, job_id)
        self.jobs: dict = {}            # job_id -> {"priority", "run_at", "attempts", "state", "token", "lease_until", "order"}
        self.dlq: list = []
        self._order = itertools.count()
        self._token = itertools.count(1)

    def submit(self, job_id, priority: int, run_at: float = 0.0) -> None:
        order = next(self._order)
        self.jobs[job_id] = {"priority": priority, "run_at": run_at, "attempts": 0, "state": "queued",
                             "token": None, "lease_until": None, "order": order}
        heapq.heappush(self.ready, (-priority, order, job_id))

    def state(self, job_id) -> str:
        """'queued' | 'leased' | 'done' | 'dead'."""
        return self.jobs[job_id]["state"]

    def _requeue_or_kill(self, job_id) -> None:
        """After a failure or expiry: DLQ if attempts >= max_attempts, else back to the ready heap."""
        j = self.jobs[job_id]
        j["token"] = None
        j["lease_until"] = None
        if j["attempts"] >= self.max_attempts:
            j["state"] = "dead"
            self.dlq.append(job_id)
        else:
            j["state"] = "queued"
            heapq.heappush(self.ready, (-j["priority"], j["order"], job_id))

    def reap(self) -> None:
        """Expire leases whose lease_until <= now (counts as a failed attempt)."""
        now = self.clock()
        for jid, j in self.jobs.items():
            if j["state"] == "leased" and j["lease_until"] <= now:
                self._requeue_or_kill(jid)

    def lease(self, worker):
        """Reap first. Return (job_id, token) for the highest-priority queued job whose run_at <= now
        (FIFO within a priority), or None. Jobs not yet runnable stay queued. attempts += 1."""
        self.reap()
        now = self.clock()
        deferred, got = [], None
        while self.ready:
            item = heapq.heappop(self.ready)
            j = self.jobs[item[2]]
            if j["state"] != "queued":
                continue
            if j["run_at"] > now:
                deferred.append(item)
                continue
            got = item[2]
            break
        for item in deferred:
            heapq.heappush(self.ready, item)
        if got is None:
            return None
        j = self.jobs[got]
        j["state"] = "leased"
        j["attempts"] += 1
        j["token"] = next(self._token)
        j["lease_until"] = now + self.lease_seconds
        j["worker"] = worker
        return got, j["token"]

    def complete(self, job_id, token) -> bool:
        """Accept only if the job is leased under this exact token and the lease has not expired."""
        j = self.jobs[job_id]
        if j["state"] != "leased" or j["token"] != token or self.clock() >= j["lease_until"]:
            return False
        j["state"] = "done"
        j["token"] = None
        return True

    def fail(self, job_id, token) -> bool:
        j = self.jobs[job_id]
        if j["state"] != "leased" or j["token"] != token:
            return False
        self._requeue_or_kill(job_id)
        return True
