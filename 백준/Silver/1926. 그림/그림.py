import sys
from collections import deque
# sys.stdin = open('test.txt')


# n 세로, m 가로
n,m = map(int,input().split())
graph = []

for idx in range(n):
    graph.append(list(map(int,input().split())))
    
dx,dy = [1,0,-1,0],[0,1,0,-1]
visited = [[False]*m for _ in range(n)]

def bfs(y,x,visited):
    arr = [(y,x)]
    pic,area = 0,0 # 그림 개수 , 넓이
    q = deque()
    q.append((y,x))
    while q:
        y,x = q.popleft()
        for i in range(4):
            ny = y+dy[i]
            nx = x+dx[i]
            if 0<=ny<n and 0<=nx<m and not visited[ny][nx] and graph[ny][nx] == 1:
                visited[ny][nx] = True
                q.append((ny,nx))
                arr.append((ny,nx))
    
    return arr

cnt,max_area = 0,0
for i in range(n):
    for j in range(m):
        if graph[i][j] == 1 and not visited[i][j]:
            visited[i][j] = True
            result = bfs(i,j,visited)
            if len(result):
                cnt += 1
                max_area = max(max_area,len(result))

print(cnt) 
print(max_area)