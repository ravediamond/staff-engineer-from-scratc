"""d22 Cheapest flights within k stops. flights = [(src, dst, price)]. At most k intermediate stops. -1 if impossible.
cheapest(4, [(0,1,100),(1,2,100),(2,0,100),(1,3,600),(2,3,200)], 0, 3, 1) == 700"""


def cheapest(n: int, flights: list, src: int, dst: int, k: int) -> int:
    INF = float("inf")
    dist = [INF] * n
    dist[src] = 0
    for _ in range(k + 1):
        nxt = dist[:]  # copy: each round adds at most one edge
        for u, v, w in flights:
            if dist[u] + w < nxt[v]:
                nxt[v] = dist[u] + w
        dist = nxt
    return -1 if dist[dst] == INF else dist[dst]
