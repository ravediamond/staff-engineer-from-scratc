# Predict

1. Fan-out 200, one billion rows. Height of the tree (levels)?
   Guess:

2. A B+tree of order 4 (max 4 keys per node). Insert 1..5 in order. What does the tree look like?
   Guess:

3. Index (tenant_id, created_at, status). Query: `WHERE tenant_id = 7 AND status = 'open'`. How many index columns narrow the scan?
   Guess:

4. Same index. `WHERE tenant_id = 7 AND created_at > now() - interval '1 day' AND status = 'open'`. How many?
   Guess:

5. Same index. `WHERE created_at > now() - interval '1 day'`. Usable?
   Guess:

6. Why do random UUID primary keys hurt a B-tree and time-ordered ids (Snowflake, UUIDv7) not?
   Guess:

## Misses
-
