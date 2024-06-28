N = int(input())
arr = list(map(int,input().split()))
result = 0
ans = []
arr.sort()
for idx in arr:
    result += idx
    ans.append(result)

print(sum(ans))