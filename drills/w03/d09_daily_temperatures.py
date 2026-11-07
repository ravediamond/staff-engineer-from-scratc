"""d09 Daily temperatures: for each day, how many days until a warmer one (0 if none). O(n).
daily_temperatures([73,74,75,71,69,72,76,73]) == [1,1,4,2,1,1,0,0]"""


def daily_temperatures(t: list) -> list:
    out = [0] * len(t)
    stack = []  # indices with decreasing temperatures
    for i, x in enumerate(t):
        while stack and t[stack[-1]] < x:
            j = stack.pop()
            out[j] = i - j
        stack.append(i)
    return out
