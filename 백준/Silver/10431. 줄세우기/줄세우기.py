# 세로,가로
T = int(input()) 

result = []
# 버블 정렬로 카운팅하기. 시간복잡도 커트라인 안넘을듯.
for k in range(T):
    arr = list(map(int,input().split()))
    cnt = 0
    for idx in range(1,len(arr)):
        for jdx in range(idx+1,len(arr)):
            # 앞에 있는 애가 더 크다면?
            temp = 0
            if arr[idx] > arr[jdx]:
                # print(arr[idx],arr[jdx])
                temp = arr[idx] # 변수 저장해주고
                arr[idx] = arr[jdx] # 뒤에 있던 애를 앞으로 넘겨주고
                arr[jdx] = temp # 저장했던 변수(=앞에 있던 애)를 뒤로 넘겨줌
                cnt += 1 # 카운팅
    
    result.append([arr[0],cnt])

for i,value in result:
    print(i,value) 