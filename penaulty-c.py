def compute(a: str) -> int:
    p = sum(1 for ch in a if ch == 'Y')
    min_p = p
    ind = 0
    for i, ch in enumerate(a):
        if ch == 'Y':
            p -= 1
        else:
            p += 1
        if p < min_p:
            min_p = p
            ind = i + 1
    return ind

s = input()
blocks = s.split()
st = []
ans = []
i = 0

for block in blocks:
    if block == "END":
        a = ""
        while len(st[-1]) == 1:
            a += st.pop()
        a_rev = a[::-1]
        min_pen = compute(a_rev)
        ans[int(st.pop()[-1])] = min_pen
    else:
        if block == "BEGIN":
            st.append(block + str(i))
            ans.append(0)
            i += 1
        else:
            st.append(block)

print(*ans)
