# Predict

1. `json.dumps({"b": 1, "a": 2})` vs `json.dumps({"a": 2, "b": 1})`: same string?
   Guess:

2. A client times out and retries a POST /charge without an idempotency key. 2% of requests time out after the charge succeeded. Out of 1M charges, how many double charges?
   Guess:

3. Is `PUT /users/42 {"name": "x"}` idempotent? Is `POST /users/42/counter/increment`?
   Guess:

4. Two retries of the same key arrive 1 ms apart, on two different servers, with a store that has no atomic "insert if absent". What can happen?
   Guess:

## Misses
-
