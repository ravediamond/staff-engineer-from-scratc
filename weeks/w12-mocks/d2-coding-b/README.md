# W12 D2: coding mock B (35 minutes, 2 problems)

## Problem B1: heavy hitters in a stream (15 min target)

Implement **Misra–Gries** with k counters: after the stream, every item with frequency > n/(k+1) is
guaranteed to be among the counters, and each counter underestimates the true count by at most n/(k+1).
Return the counters dict. (Think: top error codes, hot keys, heavy users, with bounded memory.)

## Problem B2: shortest transformation sequence (20 min target)

Given `begin`, `end` and a word list, return the number of words in the shortest sequence from begin to
end where each step changes one letter and every intermediate word is in the list; 0 if impossible.
(BFS. Think: shortest path in an implicit graph.)

## After the timer

Run the tests, then the review file: a candidate's Misra–Gries.
