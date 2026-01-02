from collections import deque
import ast

n = int(input().strip())              
r = ast.literal_eval(input().strip())
t = ast.literal_eval(input().strip()) 

g = [[] for _ in range(n)]
d = [0] * n
f = [0] * n

for u, v in r:
    u -= 1
    v -= 1
    g[u].append(v)
    d[v] += 1

q = deque()

for i in range(n):
    if d[i] == 0:
        q.append(i)
        f[i] = t[i]

while q:
    e = q.popleft()
    for ne in g[e]:
        f[ne] = max(f[ne], f[e] + t[ne])
        d[ne] -= 1
        if d[ne] == 0:
            q.append(ne)

print(max(f))
