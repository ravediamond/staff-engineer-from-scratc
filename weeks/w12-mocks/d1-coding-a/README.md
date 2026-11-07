# W12 D1: coding mock A (35 minutes, 2 problems)

Do not read the build file before the timer starts. Narrate using the W1 D1 protocol.

## Problem A1: time-versioned key-value store (15 min target)

`TimeMap.set(key, value, ts)` stores a value at a timestamp (timestamps for a key arrive in
increasing order). `TimeMap.get(key, ts)` returns the value with the **largest timestamp ≤ ts**, or `""`.
Expected: O(log n) get. (Think: feature store point-in-time lookups, config history.)

## Problem A2: task scheduler with cooldown (20 min target)

Tasks are letters; each takes one time unit; the same letter must be separated by at least `n` units
(idle allowed). Return the minimum total time to run all tasks. Expected O(len(tasks)).
(Think: rate-limited API calls per tenant.)

## After the timer

Run `uv run pytest weeks/w12-mocks/d1-coding-a -k "not review"`, then do the review file: a candidate's
TimeMap that passed their own examples. Score yourself with `rubric.md`.
