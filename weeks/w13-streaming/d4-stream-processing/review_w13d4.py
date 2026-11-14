"""Review: watermark of a job reading 3 partitions.

WHY: the watermark was the MAX over partitions. The fastest partition pushed it forward, windows closed,
and everything still waiting in the slow partition arrived "late" and was discarded. A watermark is a
promise about ALL inputs: take the minimum, and do not emit one while a partition has reported nothing
(real engines add an idle-source timeout so a silent partition cannot stall the job forever).
"""


def watermark(max_event_time_per_partition: list, max_out_of_order: int):
    if any(t is None for t in max_event_time_per_partition):
        return None
    return min(max_event_time_per_partition) - max_out_of_order
