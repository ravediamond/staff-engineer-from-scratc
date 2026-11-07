# Questions

1. Compare auto-increment, UUIDv4, UUIDv7/Snowflake for primary keys in a sharded system.
2. What must a Snowflake generator do when the clock moves backwards, and why?
3. Why does offset pagination break under writes? What does keyset pagination require of the sort key?
4. Why make cursors opaque?
5. Design the public API for an "evaluation runs" resource: create, get, list, cancel. Include idempotency, pagination and versioning.

## Model answers

1. Auto-increment: compact and ordered, but a single point of coordination per table, leaks business volume, and is hard to shard. UUIDv4: no coordination, but random inserts fragment B-trees and 128 bits is big. UUIDv7/Snowflake: no coordination, time-ordered (good index locality, rough creation-time sorting), 64 or 128 bits. Snowflake needs worker-id assignment.
2. Refuse (error, or wait until the clock passes last_ms). Generating with an earlier timestamp can reproduce an ID already issued at that ms with the same sequence. NTP slews, VM migrations and leap handling make backwards steps real.
3. OFFSET counts rows at query time, so inserts before the offset shift items into the next page (duplicates) and deletes shift them out (skips); it is also O(offset) work. Keyset pagination needs a total, stable order: a unique sort key, usually (timestamp, id), with an index on it.
4. So the server can change the sort keys, storage or encoding without breaking clients, and clients cannot forge positions. It also leaves room for signing or encrypting, to avoid leaking internal ids.
5. `POST /v1/eval-runs` with an `Idempotency-Key` header and body {model, dataset_version, metrics, config}, returning 202 + run resource {id, status, created_at, model_version}. `GET /v1/eval-runs/{id}`. `GET /v1/eval-runs?status=&model=&limit=&cursor=` with an opaque `next_cursor`. `POST /v1/eval-runs/{id}:cancel`, idempotent. URL major version, additive-only changes within it, `request_id` in every response, a deprecation policy, and status as an enum that only grows.
