"""d05 Container with most water. heights[i] are vertical lines; max area between two lines. O(n).
max_area([1,8,6,2,5,4,8,3,7]) == 49"""


def max_area(heights: list) -> int:
    i, j, best = 0, len(heights) - 1, 0
    while i < j:
        best = max(best, (j - i) * min(heights[i], heights[j]))
        if heights[i] < heights[j]:
            i += 1
        else:
            j -= 1
    return best
