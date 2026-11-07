"""Self-contained. Run after predict.md."""
c = {}
for x in "abacabda":
    if x in c:
        c[x] += 1
    elif len(c) < 2:
        c[x] = 1
    else:
        for y in list(c):
            c[y] -= 1
            if c[y] == 0:
                del c[y]
print("1.", c)
print("2. 5 (hit hot dot dog cog)")
print("3. O(N x L x 26) neighbour generations, each an O(L) string build + set lookup")
