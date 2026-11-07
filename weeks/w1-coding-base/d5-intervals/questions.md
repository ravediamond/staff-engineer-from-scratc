# Questions

1. Why is sorting by start, then comparing only with the last merged interval, correct? Why does sorting by end fail?
2. Half-open vs closed intervals: where does it change your code?
3. You run 2,000 training jobs a day with known start times and durations. How many GPUs? Then: jobs can start anywhere in a 2-hour window. What changes?
4. Calendar booking at 10k bookings/s across 1M rooms. Data structure and concurrency control?
5. How do you test interval code without trusting your own reasoning?

## Model answers

1. Sorted by start, each new interval begins at or after every earlier start, so it can only overlap the latest merged block. Anything earlier ended before that block began, or would have been merged into it. Sorted by end, a long interval that started early (`[1,10]`) arrives last, after short ones were already emitted as separate blocks it should have swallowed.
2. Overlap test (`<` vs `<=`), merge-of-touching rule, and tie-breaking in the sweep line (process ends before starts for half-open). Pick one convention, write it at the top of the file, test the boundary explicitly.
3. Fixed times: sweep line, peak concurrency = GPUs, plus headroom for failures and overruns (size for p99 duration, not mean). With flexible start windows it becomes scheduling: greedy by deadline or an ILP / list scheduler to flatten the peak, trading queueing delay for fewer GPUs. Present the curve (GPUs vs p95 wait) and let the business pick.
4. Partition by room id: each room's bookings live on one shard, so there is no cross-shard transaction. Per room, a sorted structure or an interval tree, or in a database `EXCLUDE USING gist (room WITH =, during WITH &&)` in Postgres. Concurrency via per-room serialization (row lock or single-writer actor), or optimistic insert with a constraint violation as the conflict signal. 10k/s spread over 1M rooms is low per room.
5. Property-based testing against a brute-force oracle (as these tests do): random intervals, compare with O(n²) pairwise overlap, plus invariants (output sorted, non-overlapping, same union). W11 D2 builds the tooling.
