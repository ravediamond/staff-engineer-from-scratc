"""d18 Kth largest element in a stream. KthLargest(k, nums).add(x) returns the current kth largest."""
import heapq


class KthLargest:
    def __init__(self, k: int, nums: list):
        self.k = k
        self.h = []
        for x in nums:
            self.add(x)

    def add(self, x: int) -> int:
        if len(self.h) < self.k:
            heapq.heappush(self.h, x)
        elif x > self.h[0]:
            heapq.heapreplace(self.h, x)
        return self.h[0]
