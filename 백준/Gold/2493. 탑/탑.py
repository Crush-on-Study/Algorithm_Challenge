import sys
input = sys.stdin.readline

N = int(input().rstrip())
arr = list(map(int,input().rstrip().split()))

place = [0]*N
lst = []
for idx in range(N):
    while lst:
        if lst[-1][0] < arr[idx]: # 6 < 9
            lst.pop()
            
        else:
            place[idx] = lst[-1][1]
            break
    
    lst.append((arr[idx],idx+1))
    
print(*place)