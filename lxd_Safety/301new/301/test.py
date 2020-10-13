cnt = 0
dic = {}
s = input()

dic[s] = cnt
cnt += 1

n = int(input().strip())

mp = []

for i in range(n):
    s = input().strip().split('->')
    if s[0] not in dic.keys():
        dic[s[0]] = cnt
        cnt += 1
    if s[1] not in dic.keys():
        dic[s[1]] = cnt
        cnt += 1
    while len(mp) < dic[s[0]] + 1:
        mp.append([])
    mp[dic[s[0]]].append(dic[s[1]])

vs = []
ans = 0
for i in range(cnt):
    vs.append(0)


def dfs(w):
    global ans
    global vs
    if vs[w]==1:
        return
    vs[w]=1
    ans+=1
    for c in mp[w]:
        dfs(c)
dfs(0)
print(ans-1)
C
5
A->B
B->C
C->D
E->C
C->F
