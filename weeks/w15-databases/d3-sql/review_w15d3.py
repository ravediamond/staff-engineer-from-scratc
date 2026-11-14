"""Review: the "inactive users" query behind a re-engagement email campaign.

WHY: guest orders have user_id NULL. `id NOT IN (1, 2, NULL)` is `id <> 1 AND id <> 2 AND id <> NULL`;
the last term is NULL (unknown), so the predicate is never TRUE and every row is filtered out. NOT EXISTS
compares row by row and is not affected by NULLs (filtering `WHERE user_id IS NOT NULL` in the subquery
also works).
"""

INACTIVE_USERS = """
    SELECT name
    FROM users u
    WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id)
    ORDER BY name
"""
