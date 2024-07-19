import sys
input = sys.stdin.readline

# N은 사이즈, M은 나무 정보 개수, K는 몇년 지남?
N,M,K = map(int,input().rstrip().split())

# 초기 그래프
graph = [[5]*N for _ in range(N)]

# 나무 위치
tree = [[[] for _ in range(N)] for _ in range(N)]

# 나중에 양분 추가해줄 때, 사용할 것
add_eat = [list(map(int,input().rstrip().split())) for _ in range(N)]

# 나무 정보 (y,x,나이)
for idx in range(M):
    y,x,z = map(int,input().rstrip().split())
    tree[y-1][x-1].append(z)

# 8방향 스텝
step = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]
    
#### 초기 세팅 끝 ####

# 사계절
for _ in range(K):
    for col in range(N):
        for row in range(N):
            dead = 0
            temp = []
            if tree[col][row]: # 나무가 있다면
                tree[col][row].sort() # 나이가 어린애부터
                for age in tree[col][row]:
                    if graph[col][row] >= age: # 아직 양분 줄 수 있는 경우면
                        graph[col][row] -= age # 나무 나이만큼 양분 주고
                        age += 1 # 1살 처먹음
                        temp.append(age) # 옮겨놓고
                    
                    else:
                        dead += age//2 # 뒤진 애들 나이 절반만큼 양분 흡수
                
                graph[col][row] += dead
                tree[col][row].clear() # 싹 밀어버리고
                tree[col][row].extend(temp) # 옮긴 애들 여따 박음
                
    for col in range(N):
        for row in range(N):
            if tree[col][row]:
                for age in tree[col][row]:
                    if age%5 == 0: # 5의 배수인 경우
                        for idx in step:
                            ny = col+idx[0]
                            nx = row+idx[1]
                            if 0<=ny<N and 0<=nx<N:
                                tree[ny][nx].append(1)
                                
    for col in range(N):
        for row in range(N):
            graph[col][row] += add_eat[col][row]
                
cnt = 0
for col in range(N):
    for row in range(N):
        if tree[col][row]:
            cnt += len(tree[col][row])

print(cnt)