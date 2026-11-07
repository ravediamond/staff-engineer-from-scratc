# W1 D5: intervals, booking, sweep line

Primer: `knowledge/01-python-for-interviews.md` §6. Drill pattern: "intervals".

## The one idea

Almost every interval problem is: **sort by start, then one pass with a small state.**

| Problem | Sort by | State in the pass |
|---|---|---|
| merge overlapping | start | the current merged interval |
| insert into sorted, non-overlapping | already sorted | before / overlapping / after |
| max simultaneous (rooms, concurrent jobs) | events: (+1 at start, −1 at end) | running count |
| fits in calendar (no double booking) | keep sorted, binary search neighbours | sorted list |

**Invariant for merge:** after processing intervals sorted by start up to `i`, the output is
sorted, non-overlapping, and covers exactly the union of the first `i` inputs. Sorting by start
is what makes "only compare with the last output interval" correct.

**Convention matters:** today intervals are **half-open** `[start, end)`. `[1, 3)` and `[3, 5)` do
**not** overlap (a meeting ending at 3 and one starting at 3 can share a room). For the sweep line
that means at equal times, process ends (−1) before starts (+1). Say your convention out loud in
interviews; half the bugs are here.

## Today's build (`w1d5_intervals.py`)

- `merge(intervals)` → merged, sorted (touching half-open intervals `[1,3),[3,5)` merge into `[1,5)`: they leave no gap).
- `insert(sorted_intervals, new)` → merged result, O(n).
- `max_concurrent(intervals)` → peak overlap (half-open: touching does not overlap).
- `Calendar.book(start, end)` → True and stores it if no overlap, else False. O(log n) search with `bisect`.

## Staff angle

Interval problems are capacity planning in disguise. "Max concurrent" is "how many GPUs do we
need for these training jobs", "how many DB connections at peak", "how many on-call humans". A
staff engineer asks next: which percentile is the peak? Can jobs shift (a scheduling problem,
so greedy by end time)? What happens when one job overruns? Do we size for peak or queue the excess?
