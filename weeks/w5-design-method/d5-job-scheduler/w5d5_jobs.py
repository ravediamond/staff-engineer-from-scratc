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
        # TODO
        raise NotImplementedError

    def state(self, job_id) -> str:
        """'queued' | 'leased' | 'done' | 'dead'."""
        return self.jobs[job_id]["state"]

    def _requeue_or_kill(self, job_id) -> None:
        """After a failure or expiry: DLQ if attempts >= max_attempts, else back to the ready heap."""
        # TODO
        raise NotImplementedError

    def reap(self) -> None:
        """Expire leases whose lease_until <= now (counts as a failed attempt)."""
        # TODO
        raise NotImplementedError

    def lease(self, worker):
        """Reap first. Return (job_id, token) for the highest-priority queued job whose run_at <= now
        (FIFO within a priority), or None. Jobs not yet runnable stay queued. attempts += 1."""
        # TODO
        raise NotImplementedError

    def complete(self, job_id, token) -> bool:
        """Accept only if the job is leased under this exact token and the lease has not expired."""
        # TODO
        raise NotImplementedError

    def fail(self, job_id, token) -> bool:
        # TODO
        raise NotImplementedError
