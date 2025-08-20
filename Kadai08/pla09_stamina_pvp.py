import random,sys

#変数宣言
gold = [5,5]
space = [1,1]
stamina = [6,6]
goal_space = 30
turn = 0
is_goal = False
name = ["あなた","com"]
effects = [*(["G"]*3),*(["L"]*2),*(["F"]*3),*(["B"]*2),*(["S"]*3),*(["R"]*1)]
effects += [*(["_"] * (goal_space - len(effects)))]
effects_info = "\nG: お金を得る(1~3)\nL: お金を失う(1~3)\nF: 前へ進む(1~3)\nB: 後ろへ進む(1~3)\nS: 一回休み\nR: 振出しに戻る\n"
space_eff = [None]*goal_space
p_now = [*([" "]*goal_space)]
c_now = [*([" "]*goal_space)]
p_now[0] = "1"
c_now[0] = "2"
skip = [False,False]

#ランダムにマスを設定
for i in range(goal_space):
    if i == 0 or i == goal_space-1:
        space_eff[i] = effects.pop()
    else:
        space_eff[i] = effects.pop(random.randint(0,len(effects)-2))

#<<<<<<<<<<<<<<<<<いつでも自分の現在位置を分かりやすくするためのマス表示

#現在地表示関数
def show_now():
    print(*c_now)
    print(*p_now)
    print(*space_eff)
    print()

#<<<<<<<<<<<<<<<<読みやすく分けるための横線表示

#横線を表示
def show_line():
    print("------------------------------")

#現在地を更新
def update_now():
    global space
    global turn
    x = space[turn]
    if turn == 0:
        for i in range(len(p_now)):
            p_now[i] = " "
        p_now[x-1] = "1"
    else:
        for i in range(len(c_now)):
            c_now[i] = " "
        c_now[x-1] = "2"
    show_now()

#<<<<<<<<<<<<<<<<マスの効果は全部一つの関数の中に関数を作ってまとめた

#マスの効果処理
def space_effect(eff):
    global turn
    def get_gold():
        global gold
        sumple = random.randint(1,3)
        gold[turn] += sumple
        print(f"お金獲得マスです {sumple}ゴールド獲得しました (現在{gold[turn]}ゴールド)")

    def loss_gold():
        global gold
        sumple = random.randint(1,3)
        gold[turn] -= sumple
        print(f"お金失いマスです {sumple}ゴールド失いました (現在{gold[turn]}ゴールド)")

    def move_forward():
        sumple = random.randint(1,3)
        space[turn] += sumple
        if space[turn] > goal_space:
            space[turn] = 30 - (space[turn] - 30)
        reduce_stamina(sumple)
        print(f"進みマスです {sumple}マス進みました")
        update_now()

    def move_back():
        sumple = random.randint(1,3)
        space[turn] -= sumple
        space[turn] = max(space[turn],1)
        reduce_stamina(sumple)
        print(f"戻りマスです {sumple}マス戻りました")
        update_now()

    def skip_turn():
        global skip
        skip[turn] = True
        print("一回休みマスです 次のターンは動けません")

    def restart():
        space[turn] = 1
        print(f"ふりだしマスです ふりだしに戻ってしまいました")
        update_now()

    if eff == "G":
        get_gold()
    elif eff == "L":
        loss_gold()
    elif eff == "F":
        move_forward()
    elif eff == "B":
        move_back()
    elif eff == "S":
        skip_turn()
    elif eff == "R":
        restart()
    else:
        pass

def reduce_stamina(x):
    global turn
    stamina[turn] = max(stamina[turn] - x, 1)

def chack_winner(value):
    if value[0] > value[1]:
        return name[0]
    elif value[0] < value[1]:
        return name[1]
    else:
        return "引き分け"


#すごろくMain

name[0] = input("プレイヤー１の名前を入力:")
name[1] = input("プレイヤー２の名前を入力:")
print(f"{goal_space}マスですごろくを始めます\n")
show_now()
print(effects_info)
show_line()

while not is_goal:
    if skip[turn]:
        input(f"{name[turn]}は一回休みです")
        skip[turn] = False
        turn = 1 - turn
        show_line()
        continue
    print(f"{name[turn]}の番です(ゴールド:{gold[turn]} スタミナ:{stamina[turn]})")

    #各ターン行動入力
    while True:
        x = input("[Enter]:サイコロを振る [s]:スタミナを回復(ゴールド１消費) [h]:その他のコマンド >>")
        if x == "q":
            sys.exit()
        elif x == "i":
            print(effects_info)
        elif x == "s":
            if gold[turn] > 0:
                stamina[turn] = 6
                gold[turn] -= 1
                print("ゴールドを１消費してスタミナを回復しました")
            else:
                x = "s_cant"
                print("ゴールドが足りないためスタミナを回復できません")
        elif x == "m":
            show_now()
        elif x == "h":
            print("[i]:マスの説明表示 [m]:マップと現在地を表示 [q]:ゲーム終了")
        else :
            pass
        if x == "":
            break


    #サイコロの出目分進ませる
    move = random.randint(1,stamina[turn])
    space[turn] += move
    if space[turn] > goal_space:
        space[turn] = 30 - (space[turn] - 30)
    reduce_stamina(move)
    print(f"サイコロの目は[{move}]がでました")
    update_now()

    #マスの効果処理
    space_effect(space_eff[space[turn]-1])

    #ゴールマスに到着確認
    if space[turn] == goal_space:
        is_goal = True
        first = turn
        print(f"{name[turn]}がゴールしました！")

    #スタミナもお金もなかったら強制終了
    if gold[turn] <= 0 and stamina[turn] == 1:
        first = 0 if space[0] > space[1] else 1
        stamina[turn] = 0
        print(f"{name[turn]}はおなかがすいて倒れてしまった！")
        break

    #手番交代
    turn = 1 - turn
    show_line()

show_line()
print(f"{name[0]} <マス:{space[0]} ゴールド:{gold[0]} スタミナ:{stamina[0]}>")
print(f"{name[1]} <マス:{space[1]} ゴールド:{gold[1]} スタミナ:{stamina[1]}>")
print()

gold_win = chack_winner(gold)
stamina_win = chack_winner(stamina)

print(f"スピード的勝利:{name[first]}")
print(f"金銭的勝利:{gold_win}")
print(f"スタミナ的勝利:{stamina_win}")
