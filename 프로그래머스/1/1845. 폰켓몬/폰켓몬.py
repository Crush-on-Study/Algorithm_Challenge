import copy
# 딕셔너리로 접근해보자.
def solution(nums):
    answer = 0
    dic = {}
    
    # key값 세팅
    for idx in nums:
        dic[idx] = 0
    
    # value값 세팅
    for idx in nums:
        dic[idx] += 1
    
    # 총 골라야하는 횟수
    cnt = len(nums)//2
    mod = len(nums)
    
     
    dic = dict(sorted(dic.items(), key = lambda x : x[1]))
    dic_copy = copy.deepcopy(dic)
    # dic의 출력값 {1: 1, 2: 1, 3: 2}
    
    while cnt:
        for key,value in dic.items():
            if cnt:
                dic[key] -= 1
                cnt -= 1
            else:
                break
    
    # print(dic)
    # print(dic_copy)
    for key,value in dic.items():
        if dic[key] != dic_copy[key]:
            answer += 1
    
    return answer