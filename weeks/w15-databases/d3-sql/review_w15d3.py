"""Review: the "inactive users" query behind a re-engagement email campaign. Since guest checkout shipped
(orders with no user), the campaign sends zero emails. Find the bug, fix it, explain:

WHY:
"""

INACTIVE_USERS = """
    SELECT name
    FROM users
    WHERE id NOT IN (SELECT user_id FROM orders)
    ORDER BY name
"""
