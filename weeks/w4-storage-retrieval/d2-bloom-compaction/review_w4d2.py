"""Review: compaction job. After compaction, users saw values they had overwritten weeks ago.
Find the bug, fix it, explain:

WHY:
"""


def compact(runs_newest_first):
    merged = {}
    for run in runs_newest_first:
        for k, v in run:
            merged[k] = v
    return sorted(merged.items())
