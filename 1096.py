from collections import deque

def brace(sg):
    q = deque([sg])
    out = set()

    while q:
        s = q.popleft()

        l = -1
        r = 0
        while r < len(s) and s[r] != '}':
            if s[r] == '{':
                l = r
            r += 1

        if l == -1:
            out.add(s)
            continue

        prefix = s[:l]
        suffix = s[r+1:]
        inner = s[l+1:r].split(',')

        for w in inner:
            q.append(prefix + w + suffix)

    return sorted(out)
expr=input()
print(brace(expr))
