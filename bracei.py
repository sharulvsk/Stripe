o=[]
def dfs(sq,j,n):
    if j==len(sq):
        o.append(n)
        return
    for ch in sq[j]:
        dfs(sq,j+1,n+ch)
s=input()
i=0
sq=[]
c=[]
while i<len(s):
    if s[i]=='{':
        if c:
            sq.append(c)
            c=[]
    elif s[i]=='}':
        sq.append(c)
        c=[]
    elif s[i]!=',':
        c.append(s[i])
    i+=1
if c:
    sq.append(c)
dfs(sq,0,"")
for k in o:
    print(k)
