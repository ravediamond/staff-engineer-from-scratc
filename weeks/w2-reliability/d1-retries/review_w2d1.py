"""Review: a retry helper from a PR titled 'make tool calls more robust'.
It made an outage worse. Find the bug, fix it, explain:

WHY:
"""


class HTTPError(Exception):
    def __init__(self, status):
        super().__init__(status)
        self.status = status


RETRYABLE = {429, 500, 502, 503, 504}


def call(fn, attempts, sleep, delays):
    for i in range(attempts):
        try:
            return fn()
        except HTTPError as e:
            if e.status not in RETRYABLE or i == attempts - 1:
                raise
            sleep(delays[i])
