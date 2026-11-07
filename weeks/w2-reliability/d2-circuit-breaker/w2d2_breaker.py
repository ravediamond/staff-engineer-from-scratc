"""W2 D2: circuit breaker with closed / open / half-open states and an injected clock."""

CLOSED, OPEN, HALF_OPEN = "closed", "open", "half_open"


class CircuitOpen(Exception):
    pass


class CircuitBreaker:
    def __init__(self, failure_threshold: int, reset_timeout: float, half_open_max: int,
                 success_threshold: int, clock):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.half_open_max = half_open_max
        self.success_threshold = success_threshold
        self.clock = clock
        self._state = CLOSED
        self.failures = 0
        self.opened_at = 0.0
        self.in_flight = 0       # trial calls admitted in HALF_OPEN and not yet recorded
        self.half_successes = 0

    @property
    def state(self) -> str:
        """Current state; OPEN turns into HALF_OPEN once reset_timeout has elapsed."""
        if self._state == OPEN and self.clock() >= self.opened_at + self.reset_timeout:
            self._state = HALF_OPEN
            self.in_flight = 0
            self.half_successes = 0
        return self._state

    def _open(self) -> None:
        self._state = OPEN
        self.opened_at = self.clock()
        self.failures = 0
        self.in_flight = 0
        self.half_successes = 0

    def allow(self) -> bool:
        s = self.state
        if s == CLOSED:
            return True
        if s == OPEN:
            return False
        if self.in_flight < self.half_open_max:
            self.in_flight += 1
            return True
        return False

    def record_success(self) -> None:
        s = self.state
        if s == CLOSED:
            self.failures = 0
        elif s == HALF_OPEN:
            self.in_flight = max(0, self.in_flight - 1)
            self.half_successes += 1
            if self.half_successes >= self.success_threshold:
                self._state = CLOSED
                self.failures = 0

    def record_failure(self) -> None:
        s = self.state
        if s == CLOSED:
            self.failures += 1
            if self.failures >= self.failure_threshold:
                self._open()
        elif s == HALF_OPEN:
            self._open()

    def call(self, fn):
        if not self.allow():
            raise CircuitOpen()
        try:
            out = fn()
        except Exception:
            self.record_failure()
            raise
        self.record_success()
        return out
