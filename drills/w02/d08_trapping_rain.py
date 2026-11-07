"""d08 Trapping rain water, O(n) time, O(1) extra space.
trap([0,1,0,2,1,0,1,3,2,1,2,1]) == 6"""


def trap(h: list) -> int:
    i, j = 0, len(h) - 1
    lmax = rmax = water = 0
    while i < j:
        if h[i] < h[j]:
            lmax = max(lmax, h[i])
            water += lmax - h[i]
            i += 1
        else:
            rmax = max(rmax, h[j])
            water += rmax - h[j]
            j -= 1
    return water
