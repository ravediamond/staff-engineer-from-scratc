"""Review: watermark of a job reading 3 partitions. The hourly revenue report is too low on days when one
partition lags (a broker was slow): its events are discarded as "late". Find the bug, fix it, explain:

WHY:
"""


def watermark(max_event_time_per_partition: list, max_out_of_order: int):
    seen = [t for t in max_event_time_per_partition if t is not None]
    if not seen:
        return None
    return max(seen) - max_out_of_order
