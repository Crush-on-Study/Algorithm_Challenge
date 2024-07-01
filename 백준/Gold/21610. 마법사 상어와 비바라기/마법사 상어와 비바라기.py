from collections import deque

N,M = map(int,input().split())
graph = []
for _ in range(N):
    graph.append(list(map(int,input().split())))

cmd = []
for _ in range(M):
    d,s = map(int,input().split())
    cmd.append((d-1,s))
    
#     ←,  ↖, ↑, ↗, →, ↘,  ↓ , ↙
dx = [-1,-1, 0, 1, 1,  1, 0, -1]
dy = [0, -1,-1,-1, 0,  1, 1, 1]

# 구름 위치
cloud = deque([[N-2,0],[N-2,1],[N-1,0],[N-1,1]])

# 1번 행동 : 구름 이동
def first(d,s,cloud,visited):
    new_cloud = deque()
    while cloud:
        cy,cx = cloud.popleft()
        ny = (cy + dy[d]*s)%N
        nx = (cx + dx[d]*s)%N
        new_cloud.append((ny,nx))
        visited[ny][nx] = True # 비구름    
    
    return new_cloud,visited
    
# 2번 행동 : 비구름
def second(new_cloud,graph):
    for yy,xx in new_cloud:
        graph[yy][xx] += 1
    
    return graph
    
# 3번 행동 : 비구름 있던 곳에서 대각선 방향으로 물 주기.
def third(new_cloud,graph):
    # ↖ , ↗ , ↘ , ↙
    cxx = [-1,1,1,-1]
    cyy = [-1,-1,1,1]
    while new_cloud:
        cnt = 0
        cy,cx = new_cloud.popleft()
        for i in range(4):
            nny = cy+cyy[i]
            nnx = cx+cxx[i]
            if 0<=nny<N and 0<=nnx<N and graph[nny][nnx] != 0:
                cnt += 1
            
        if cnt > 0:
            graph[cy][cx] += cnt
    
    return graph
    
# 4번 행동 : 물의 양이 2 이상인 곳 (원래 있던 구름 제외) 에 새로운 구름 생기고 -2
def forth(visited,cloud):
    cloud = deque()
    for idx in range(N):
        for jdx in range(N):
            if graph[idx][jdx] >= 2 and not visited[idx][jdx]:
                visited[idx][jdx] = True
                graph[idx][jdx] -= 2
                cloud.append((idx,jdx))
    
    return cloud


# ccnt = 0
for d,s in cmd:
    # if ccnt >= 2:
    #     break
    visited = [[False]*N for _ in range(N)] # 비구름 위치 확인할 그래프
    new_cloud,visited = first(d,s,cloud,visited)
    graph = second(new_cloud,graph)
    graph = third(new_cloud,graph)
    cloud = forth(visited,cloud)
    # ccnt += 1
    
answer = 0
for idx in range(N):
    for jdx in range(N):
        answer += graph[idx][jdx]

print(answer)