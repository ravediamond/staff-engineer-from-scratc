"""W11 D1: flaky-aware bisection, change-point detection, event correlation."""
import bisect
import statistics


def majority(results: list) -> bool:
    """True if strictly more than half are True."""
    return sum(results) * 2 > len(results)


def bisect_first_bad(n: int, is_bad, repeats: int = 1) -> tuple:
    """Versions 0..n-1; version 0 is known good, n-1 known bad. is_bad(i) may be flaky: decide each probe by
    majority over `repeats` calls. Return (first bad index, number of is_bad calls)."""
    calls = 0
    lo, hi = 0, n - 1  # invariant: lo good, hi bad
    while hi - lo > 1:
        mid = (lo + hi) // 2
        votes = [is_bad(mid) for _ in range(repeats)]
        calls += repeats
        if majority(votes):
            hi = mid
        else:
            lo = mid
    return hi, calls


def change_point(series: list, baseline_n: int, k: float = 3.0):
    """First index i >= baseline_n with series[i] > mean + k * stdev of series[:baseline_n] (sample stdev).
    None if never."""
    base = series[:baseline_n]
    thr = statistics.fmean(base) + k * statistics.stdev(base)
    for i in range(baseline_n, len(series)):
        if series[i] > thr:
            return i
    return None


def last_event_before(t, events: list):
    """events: sorted list of (time, name). The last event with time <= t, or None."""
    times = [e[0] for e in events]
    i = bisect.bisect_right(times, t)
    return events[i - 1] if i else None
