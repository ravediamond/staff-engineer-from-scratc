"""Review: an idempotency middleware. A customer reused a key by mistake for a second, larger payment
and got a 'success' response with the first payment's receipt. Find the bug, fix it, explain:

WHY:
"""
import hashlib
import json


class Conflict(Exception):
    pass


class Middleware:
    def __init__(self):
        self.done = {}  # key -> (fingerprint, response)

    def handle(self, key, body, handler):
        fp = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()
        if key in self.done:
            stored_fp, response = self.done[key]
            if stored_fp != fp:
                raise Conflict(key)
            return response
        response = handler(body)
        self.done[key] = (fp, response)
        return response
