"""Self-contained. Run after predict.md."""
a = b = 0
a += 1; ea = a          # A local event
a += 1; send = a        # A send
b += 1; eb = b          # B local event
b = max(b, send) + 1    # B receive
print("1. Lamport: A event", ea, "A send", send, "B event", eb, "B receive", b)


def cmp(x, y):
    ks = x.keys() | y.keys()
    le = all(x.get(k, 0) <= y.get(k, 0) for k in ks)
    ge = all(x.get(k, 0) >= y.get(k, 0) for k in ks)
    return "equal" if le and ge else "before" if le else "after" if ge else "concurrent"


print("2.", cmp({"a": 2, "b": 1}, {"a": 1, "b": 2}))
print("3.", cmp({"a": 1}, {"a": 1, "b": 1}))
print("4. three concurrent versions {r1:1}, {r2:1}, {r3:1}: none dominates -> 3 siblings")
