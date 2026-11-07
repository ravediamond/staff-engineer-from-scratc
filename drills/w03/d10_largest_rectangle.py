"""d10 Largest rectangle in a histogram. O(n).
largest_rectangle([2,1,5,6,2,3]) == 10"""


def largest_rectangle(h: list) -> int:
    stack, best = [], 0  # indices with increasing heights
    for i, x in enumerate(h + [0]):
        start = i
        while stack and stack[-1][1] > x:
            idx, height = stack.pop()
            best = max(best, height * (i - idx))
            start = idx
        stack.append((start, x))
    return best
