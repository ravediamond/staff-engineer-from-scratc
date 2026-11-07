"""W11 D1: flaky-aware bisection, change-point detection, event correlation."""
import bisect
import statistics


def majority(results: list) -> bool:
    """True if strictly more than half are True."""
    # TODO
    raise NotImplementedError


def bisect_first_bad(n: int, is_bad, repeats: int = 1) -> tuple:
    """Versions 0..n-1; version 0 is known good, n-1 known bad. is_bad(i) may be flaky: decide each probe by
    majority over `repeats` calls. Return (first bad index, number of is_bad calls)."""
    # TODO
    raise NotImplementedError


def change_point(series: list, baseline_n: int, k: float = 3.0):
    """First index i >= baseline_n with series[i] > mean + k * stdev of series[:baseline_n] (sample stdev).
    None if never."""
    # TODO
    raise NotImplementedError


def last_event_before(t, events: list):
    """events: sorted list of (time, name). The last event with time <= t, or None."""
    # TODO
    raise NotImplementedError
