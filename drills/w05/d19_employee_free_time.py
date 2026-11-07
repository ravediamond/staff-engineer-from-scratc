"""d19 Employee free time. schedules[i] = sorted, non-overlapping [start, end) intervals of employee i.
Return the finite free intervals common to all employees, sorted.
free_time([[[1,2],[5,6]], [[1,3]], [[4,10]]]) == [[3,4]]"""
import heapq


def free_time(schedules: list) -> list:
    heap = [(s[0][0], s[0][1], i, 0) for i, s in enumerate(schedules) if s]
    heapq.heapify(heap)
    out = []
    end = None
    while heap:
        s, e, i, j = heapq.heappop(heap)
        if end is not None and s > end:
            out.append([end, s])
        end = e if end is None else max(end, e)
        if j + 1 < len(schedules[i]):
            ns, ne = schedules[i][j + 1]
            heapq.heappush(heap, (ns, ne, i, j + 1))
    return out
