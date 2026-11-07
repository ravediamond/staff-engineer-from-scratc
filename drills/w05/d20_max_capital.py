"""d20 Maximise capital: start with capital w, do at most k projects; project i needs capital[i] and adds profit[i].
Return the final capital. (Greedy with two heaps.)
max_capital(2, 0, [1,2,3], [0,1,1]) == 4"""
import heapq


def max_capital(k: int, w: int, profits: list, capital: list) -> int:
    projects = sorted(zip(capital, profits))
    avail, i = [], 0
    for _ in range(k):
        while i < len(projects) and projects[i][0] <= w:
            heapq.heappush(avail, -projects[i][1])
            i += 1
        if not avail:
            break
        w -= heapq.heappop(avail)
    return w
