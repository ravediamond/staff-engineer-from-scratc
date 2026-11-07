# Questions

1. Why is a lease-based lock unsafe on its own? Give the timeline.
2. How do fencing tokens fix it, and what must the storage support?
3. Your storage is S3 (no compare on a custom token). How do you fence checkpoint writes from two trainers?
4. Agents pull tasks from a queue with a 5-minute visibility timeout. A task takes 7 minutes. What happens and how do you fix it?
5. When is "just use a lock" the wrong design entirely?

