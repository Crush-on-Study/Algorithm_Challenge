a,b = map(int,input().split())
arr = list(map(int,input().split()))

# a는 카드 개수, b는 목표값

arr = sorted(arr)
result = []

for i in range(len(arr)):
    for j in range(i+1,len(arr)):
        for k in range(j+1,len(arr)):
            if arr[i]+arr[j]+arr[k] <= b:
                result.append(arr[i]+arr[j]+arr[k])

print(max(result))