# Predict

1. `SELECT COUNT(*), COUNT(shipped_at) FROM orders`: 10 rows, 4 with `shipped_at` NULL. Result?
   Guess:

2. `SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM orders)` where one order has `user_id` NULL. How many rows?
   Guess:

3. `users LEFT JOIN orders ON … WHERE orders.status = 'paid'`: are users with no orders in the result?
   Guess:

4. orders (1 row per order) joined to items (3 rows per order) joined to payments (2 rows per order), then `SUM(payments.amount)`. By what factor is the sum wrong?
   Guess:

5. Can you write `WHERE ROW_NUMBER() OVER (…) = 1`?
   Guess:

## Misses
-
