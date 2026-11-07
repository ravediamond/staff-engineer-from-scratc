"""Review: a teammate's PR adding retries to the eval runner. Read it as a code reviewer: find the bug, fix it,
and write the review comment you would leave:

WHY:
"""


class TransientError(Exception):
    pass


def call_with_retries(fn, retries):
    attempt = 0
    while True:
        attempt += 1
        try:
            return fn(), attempt
        except Exception:
            if attempt > retries:
                raise
