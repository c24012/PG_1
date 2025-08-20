
#変数の定義
board = [[0]*10 for _ in range(10)]
pos = [1,2]
vec = 1
in_num = 0
balls_ans = [None]

#<<<<<<<<<<<<<<端に着いたときにIndexエラーにならないように端にも番号を付けておく
#<<<<<<<<<<<<<<端の番号は光をあてる番号+100を使い、判断時に利用できるようにする

#盤面の作成
def MakeBoard():
    #盤の周りに番号＋100を設定
    for i in range(1,9):
        board[0][i] = 100 + i
        board[i][9] = 100 + i + 8
        board[9][9-i] = 100 + i + 8 * 2
        board[9-i][0] = 100 + i + 8 * 3
    #４つ角には100を割り当てる
    for y in range(2):
        for x in range(2):
            board[y*9][x*9] = 100

#<<<<<<<<<<<<<見た目を見やすくするための横線

#横線の表示
def ShowLine():
    print("-----------------------------------------------")

#<<<<<<<<<<<<<見た目で分かりやすくするため、マスと番号を表示できるようにする
#<<<<<<<<<<<<<表の表示のオプションとして答え表示用とマス指定を分かりやすくするフラグを追加

#盤面の表示
def ShowBoard(ans=False,pos=False):
    print("")
    for y in range(10):
        for x in range(10):
            space = board[x][y]
            if space == 0 or space == 1:
                if ans:
                    print(f"{"○" if space == 0 else "●"}",end="  ")
                else:
                    print("○",end="  ")
            elif space > 100:
                space -= 100
                if pos:
                    if space < 9:
                        print(f"{space}",end=" ")
                    elif space < 25:
                        pass
                    else:
                        print(f"{33-space}",end="  ")
                else:
                    print(f"{space}",end=" ")
            else:
                print(" ",end=" ")
        print("")
    print("")

#<<<<<<<<<<<<<<<<<<<ボールの配置を入力してもらう形として[x1,y1 x2,y2]という方式を使った
#<<<<<<<<<<<<<<<<<<<他人にやってもらったら理解が難しそうだったから、もっといい入力方法があるかも知れない...

#ボールの配置
def SetBall():
    global balls_ans
    print("ボールを設置する場所を５つまで指定してください")
    print("入力は[x,y]の形で入力してください(左上角を1,1とします)")
    print("入力例:1,1 2,2 3,3 4,4 5,5")
    balls_ans = [[int(b) for b in a.split(",")] for a in input(":").split()]
    for ball_pos in balls_ans:
        board[ball_pos[0]][ball_pos[1]] = 1
    print("ボールを配置しました")

#<<<<<<<<<<<<<<<<<<<光をあてる番号を入力してもらい、番号によって度の向きに進のかをvecとして設定しておく

#光をあてる番号を指定
def SetStart():
    global in_num
    global pos
    global vec  
    while True:
        in_num = int(input("何番から光をあてますか？(0:回答 -1:おわる):"))
        if in_num >= -1 and in_num <= 32:
            break
    #解答とおわる場合返却
    if in_num == 0 or in_num == -1:
        return in_num
    #番号によって始めの位置と進む方向を指定
    if in_num < 9:
        vec = 1
        pos = [1,in_num]
    elif in_num < 17:
        vec = 0
        pos = [in_num-8,8]
    elif in_num < 25:
        vec = 3
        pos = [8,9-(in_num-8*2)]
    else:
        vec = 2
        pos = [9-(in_num-8*3),1]
    print(f"{in_num}番からの光は",end="")
    return 1

#<<<<<<<<<<<<<<<<<光の方向によって進む前にボールが干渉しているかを上下左右4パターンで確認している
#<<<<<<<<<<<<<<<<<４パターンの関数が部分的に被っている処理があるため、何とか一つにまとめたい...

#光が進む処理
def Move():
    #光が吸収されたフラグ
    fin = False
    
    #上へ進む
    def Up():
        global vec
        if board[pos[0]][pos[1]] == 1:
            return True
        elif board[pos[0]+1][pos[1]] == 1 or board[pos[0]-1][pos[1]] == 1:
            vec = 2
        elif board[pos[0]-1][pos[1]-1] == 1:
            vec = 1
        elif board[pos[0]+1][pos[1]-1] == 1:
            vec = 3
        return False

    #右へ進む
    def Right():
        global vec
        if board[pos[0]][pos[1]] == 1:
            return True
        elif board[pos[0]][pos[1]-1] == 1 or board[pos[0]][pos[1]+1] == 1:
            vec = 3
        elif board[pos[0]+1][pos[1]-1] == 1:
            vec = 2
        elif board[pos[0]+1][pos[1]+1] == 1:
            vec = 0
        return False

    #下へ進む
    def Down():
        global vec
        if board[pos[0]][pos[1]] == 1:
            return True
        elif board[pos[0]+1][pos[1]] == 1 or board[pos[0]-1][pos[1]] == 1:
            vec = 0
        elif board[pos[0]+1][pos[1]+1] == 1:
            vec = 1
        elif board[pos[0]-1][pos[1]+1] == 1:
            vec = 3
        return False

    #左へ進む
    def Left():
        global vec
        if board[pos[0]][pos[1]] == 1:
            return True
        elif board[pos[0]][pos[1]+1] == 1 or board[pos[0]][pos[1]-1] == 1:
            vec = 1
        elif board[pos[0]-1][pos[1]-1] == 1:
            vec = 2
        elif board[pos[0]-1][pos[1]+1] == 1:
            vec = 0
        return False

    #進行方向によって実行する関数を呼ぶ
    while True:
        if vec == 0:
            fin = Up()
        elif vec == 1:
            fin = Right()
        elif vec == 2:
            fin = Down()
        elif vec == 3:
            fin = Left()
        #進行方向に進ませる
        if vec == 0:
           pos[1] -= 1
        elif vec == 1:
            pos[0] += 1
        elif vec == 2:
            pos[1] += 1
        elif vec == 3:
            pos[0] -= 1
        print(vec)
        #吸収されたら終了
        if fin:
            print("吸収された")
            break
        #端に着いていても終了
        elif board[pos[0]][pos[1]] > 100:
            if board[pos[0]][pos[1]] == in_num + 100:
                print("反射された")
            else:
                print(f"{board[pos[0]][pos[1]]-100}番から抜けた")
            break

#<<<<<<<<<<<<<<<入力された答えが同順でなくとも一致してるか判断するために、どちらも並び替えを行って同じ順番にする

#回答関数
def Answer():
    print(f"ボールがある場所を入力してください(ボール:{len(balls_ans)}個 不同順OK)")
    print("入力は[x,y]の形で入力してください(左上角を1,1とします)")
    print("入力例:1,1 2,2 3,3 4,4 5,5")
    ans = [[int(b) for b in a.split(",")] for a in input(":").split()]
    #順番違い防止のための並べ替え
    ans.sort()
    balls_ans.sort()
    #合っているか確認
    if ans == balls_ans:
        print("正解です！！")
        return True
    else:
        print("違います...")
        x = input("ゲームを続けますか？(Yes:enter,y No:n)")
        if x == "n":
            return True
        else:
            return False

#---Main---#

print("+++++ブラックボックス+++++")
MakeBoard()
ShowBoard(pos=True)
SetBall()
for i in range(100):
    print("")
print("ここからは解答者が光線をあてたい数字を入力してください")
count = 0
while True:
    ShowLine()
    ShowBoard()
    result = SetStart()
    if result == 1:
        Move()
        count += 1
    elif result == 0:
        ShowLine()
        ShowBoard(pos=True)
        fin = Answer()
        if fin:
            print("-----答え-----")
            ShowBoard(ans=True)
            print(f"光を照射した回数:{count}")
            break
    elif result == -1:
        break
print("+++++ブラックボックスを終了します+++++")
