import sys
# sys.stdin = open('test.txt')
input = sys.stdin.readline

N,M = map(int, input().rstrip().split())
graph = []
for _ in range(N):
    graph.append(list(input().rstrip()))
command = list(input().rstrip())

character_pos_before = '.'
killer = ""
monster_count = 0
item_box_count = 0
turn_count = 0

for i in range(N):
    for j in range(M):
        if graph[i][j] == '&' or graph[i][j] == 'M':
            monster_count += 1
        elif graph[i][j] == '@':
            start_row, start_col = i, j
        elif graph[i][j] == 'B':
            item_box_count += 1

monster_info = [[dict() for _ in range(M)] for _ in range(N)]
for _ in range(monster_count):
    r, c, s, w, a, h, e = input().rstrip().split()

    monster_info[int(r)-1][int(c)-1] = {
        "name": s,
        "atk": int(w),
        "def": int(a),
        "hp": int(h),
        "exp": int(e)
    }

item_info = [[dict() for _ in range(M)] for _ in range(N)]
for _ in range(item_box_count):
    r, c, t, s = input().rstrip().split()
    if t == 'W' or t == 'A':
        item_info[int(r) - 1][int(c) - 1] = {
            "type": t,
            "val": int(s)
        }
    else:
        item_info[int(r) - 1][int(c) - 1] = {
            "type": t,
            "val": s
        }

character_info = {
    "level": 1,
    "max_hp": 20,
    "hp": 20,
    "atk": 2,
    "def": 2,
    "exp": 0,
    "max_exp": 5,
    "weapon": 0,
    "armor": 0,
    "accessory_count": 0,
    "HR": False,
    "RE": False,
    "CO": False,
    "EX": False,
    "DX": False,
    "HU": False,
    "CU": False
}


def Battle(row, col, is_boss=False):
    global character_pos_before, killer
    is_first_atk = True
    is_no_damage = False
    ch_atk = character_info["atk"] + character_info["weapon"]
    ch_def = character_info["def"] + character_info["armor"]
    monster = monster_info[row][col]
    monster_max_hp = monster["hp"]

    # HU 장신구 효과 적용
    if is_boss and character_info["HU"]:
        character_info["hp"] = character_info["max_hp"]
        is_no_damage = True

    while True:
        # 데미지 계산
        if is_first_atk and character_info["CO"]:
            if character_info["DX"]:
                character_damage = max(1, 3*ch_atk - monster["def"])
            else:
                character_damage = max(1, 2*ch_atk - monster["def"])
            is_first_atk = False
        else:
            character_damage = max(1, ch_atk - monster["def"])

        monster_damage = max(1, monster["atk"] - ch_def)

        # 캐릭터 공격
        monster["hp"] -= character_damage

        # 몬스터가 죽었을 때
        if monster["hp"] <= 0:
            character_pos_before = '.'
            if character_info["HR"]:
                character_info["hp"] = min(character_info["hp"] + 3, character_info["max_hp"])

            # 경험치 계산
            if character_info["EX"]:
                get_exp = int(monster["exp"]*1.2)
            else:
                get_exp = monster["exp"]
            character_info["exp"] += get_exp
            # 레벨 업
            if character_info["exp"] >= character_info["max_exp"]:
                character_info["level"] += 1
                character_info["exp"] = 0
                character_info["max_exp"] += 5
                character_info["atk"] += 2
                character_info["def"] += 2
                character_info["max_hp"] += 5
                character_info["hp"] = character_info["max_hp"]

            if is_boss:
                return "clear"
            return "win"

        if is_no_damage:
            is_no_damage = False
        else:
            character_info["hp"] -= monster_damage

        # 캐릭터가 죽었을 때
        if character_info["hp"] <= 0:
            character_info["hp"] = 0
            monster_info[now_row][now_col]["hp"] = monster_max_hp
            killer = monster["name"]
            return "dead"


def Event(row, col):
    global character_pos_before, character_info, killer
    event = graph[row][col]

    # 만약 현재 위치 그대로 이벤트가 발생한 경우
    if event == '@':
        event = character_pos_before
    else:
        character_pos_before = event
        # 이동한 캐릭터 지도에 표시
        graph[row][col] = '@'

    if event == '.':
        return "blank"

    elif event == '&':
        return Battle(row, col)

    elif event == 'B':
        # 아이템 획득, 및 착용
        get_item = item_info[row][col]
        if get_item["type"] == "W":
            character_info["weapon"] = get_item["val"]
        elif get_item["type"] == "A":
            character_info["armor"] = get_item["val"]
        elif get_item["type"] == "O":
            if character_info["accessory_count"] < 4:
                if not character_info[get_item["val"]]:
                    character_info[get_item["val"]] = True
                    character_info["accessory_count"] += 1

        # 상자를 열면 해당 칸이 빈칸이 된다.
        character_pos_before = '.'

    elif event == '^':
        # 가시 데미지 분기
        damage = 5
        if character_info["DX"]:
            damage = 1

        # 데미지 계산
        character_info["hp"] -= damage

        # 사망 처리
        if character_info["hp"] <= 0:
            character_info["hp"] = 0
            killer = "SPIKE TRAP"
            return "dead"

    elif event == 'M':
        return Battle(row, col, True)

    # 벽은 밖에서 처리
    elif event == '#':
        assert True


now_row, now_col = start_row, start_col
result_message = ""
for cmd in command:
    turn_count += 1
    before_row, before_col = now_row, now_col
    graph[before_row][before_col] = character_pos_before

    if cmd == 'L':
        now_col = max(0, now_col-1)
    elif cmd == 'R':
        now_col = min(M-1, now_col+1)
    elif cmd == 'U':
        now_row = max(0, now_row-1)
    elif cmd == 'D':
        now_row = min(N-1, now_row+1)

    if graph[now_row][now_col] == '#':
        now_row, now_col = before_row, before_col

    event_result = Event(now_row, now_col)

    if event_result == 'clear':
        result_message = "YOU WIN!"
        break

    elif event_result == 'dead':
        # 부활 장신구 처리
        if character_info["RE"]:
            character_info["RE"] = False
            character_info["accessory_count"] -= 1
            character_info["hp"] = character_info["max_hp"]
            # 게임 시작 위치로 이동
            graph[now_row][now_col] = character_pos_before
            now_row, now_col = start_row, start_col
            character_pos_before = '.'
            graph[now_row][now_col] = '@'

        # 부활 장신구가 없을 경우 게임 끝
        else:
            graph[now_row][now_col] = character_pos_before
            result_message = f"YOU HAVE BEEN KILLED BY {killer}.."
            break

if result_message == "":
    result_message = "Press any key to continue."
for i in range(N):
    print("".join(graph[i]))
print(f"Passed Turns : {turn_count}")
print("LV", ":", character_info["level"])
print("HP", ":", str(character_info["hp"])+'/'+str(character_info["max_hp"]))
print("ATT", ":", str(character_info["atk"]) + '+' + str(character_info["weapon"]))
print("DEF", ":", str(character_info["def"]) + '+' + str(character_info["armor"]))
print("EXP", ":", str(character_info["exp"])+'/'+str(character_info["max_exp"]))
print(result_message)