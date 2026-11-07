"""d12 Decode string: k[encoded] repeats encoded k times, nesting allowed.
decode("3[a2[c]]") == "accaccacc" """


def decode(s: str) -> str:
    stack, cur, num = [], "", 0
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch == "[":
            stack.append((cur, num))
            cur, num = "", 0
        elif ch == "]":
            prev, k = stack.pop()
            cur = prev + cur * k
        else:
            cur += ch
    return cur
