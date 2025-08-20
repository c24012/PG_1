
#変数の定義
board = [[0]*10 for _ in range(10)]
pos = [1,2]
vec = [0,0]
in_num = 0
balls_ans = []

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

#横線の表示
def ShowLine():
    print("-----------------------------------------------")

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

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<想定外の入力でのエラーを対策

#ボールの配置
def SetBall():
    global balls_ans
    print("ボールを設置する場所を５つまで指定してください")
    print("入力は[x,y]の形で入力してください(左上角を1,1とします)")
    print("入力例:1,1 2,2 3,3 4,4 5,5")
    while True:
        try:
            ans = [[int(b) for b in a.split(",")] for a in input(":").split()]
            for i in ans:
                try:
                    if i[0] < 1 or i[0] > 8 or i[1] < 1 or i[1] > 8:
                        print("1~8の整数を入力してください")
                        break
                except IndexError:
                    print("入力エラーです 再入力してください")
                    break
            else:
                for pos in ans:
                    if pos not in balls_ans:
                        balls_ans.append(pos)
                break
        except ValueError:
            print("入力エラーです 再入力してください") 
    for ball_pos in balls_ans:
        board[ball_pos[0]][ball_pos[1]] = 1
    print("ボールを配置しました")

#光をあてる番号を指定
def SetNumber():
    global in_num
    global pos
    global vec  
    while True:
        try:
            in_num = int(input("何番から光をあてますか？(0:回答(何度でも可能) -1:おわる):"))
            if in_num >= -1 and in_num <= 32:
                break
         #数字以外の入力は無視
        except: 
            pass
    #解答とおわる場合返却
    if in_num == 0 or in_num == -1:
        return in_num
    #番号によって始めの位置と進む方向を指定
    if in_num < 9:
        vec = [1,0]
        pos = [1,in_num]
    elif in_num < 17:
        vec = [0,-1]
        pos = [in_num-8,8]
    elif in_num < 25:
        vec = [-1,0]
        pos = [8,9-(in_num-8*2)]
    else:
        vec = [0,1]
        pos = [9-(in_num-8*3),1]
    print(f"{in_num}番からの光は",end="")
    return 1

#光が進む処理
def Move():
    #光が吸収されたフラグ
    fin = False
    first = True

    #ボールに干渉するか確認して進む方向を回転
    def CheckBallAndTurnVec():
        """
        return bool 進行を終了するか否か
        """
        global vec
        #今いる場所にボールがある場合進行を中止
        if board[pos[0]][pos[1]] == 1:
            return True
        #最初だけ横にボールがある場合方向を反転
        if first:
            if vec[0] == 0:
                if board[pos[0]+1][pos[1]] == 1 or board[pos[0]-1][pos[1]] == 1:
                    vec[1] *= -1
                    return False
            else:
                if board[pos[0]][pos[1]+1] == 1 or board[pos[0]][pos[1]-1] == 1:
                    vec[0] *= -1
                    return False

#<<<<<<<<<<<<<<<<<<<<<<<<<<似た処理の関数の共通部分をまとめた

        #右上の確認[上,右]
        if vec[0] == -1 or vec[1] == 1:
            if board[pos[0]+1][pos[1]-1] == 1:
                vec = [vec[1],vec[0]]
        #右下の確認[下,右]
        if vec[0] == 1 or vec[1] == 1:
            if board[pos[0]+1][pos[1]+1] == 1:
                vec = [-vec[1],-vec[0]]
        #左下の確認[下,左]
        if vec[0] == 1 or vec[1] == -1:
            if board[pos[0]+1][pos[1]-1] == 1:
                vec = [vec[1],vec[0]]
        #左上の確認[上,左]
        if vec[0] == -1 or vec[1] == -1:
            if board[pos[0]-1][pos[1]-1] == 1:
                vec = [-vec[1],-vec[0]]
        return False

#<<<<<<<<<<<<<<<<<<<まとめたことで方向によって関数を呼び分けなくても良くなった

    #進行方向によって実行する関数を呼ぶ
    while True:
        fin = CheckBallAndTurnVec()
        #進行方向に進ませる
        pos[0] += vec[0]
        pos[1] += vec[1]
        print(pos)
        #吸収されたら終了
        if fin:
            input("吸収された <enter>")
            break
        #端に着いていても終了
        elif board[pos[0]][pos[1]] > 100:
            #今いる場所がはじめと同じ場所であれば反射
            if board[pos[0]][pos[1]] == in_num + 100:
                input("反射された <enter>")
            #異なる場合は抜け
            else:
                input(f"{board[pos[0]][pos[1]]-100}番から抜けた <enter>")
            break
        #続く場合はfirstフラグをオフ
        first = False

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<上と同じように入力エラーを対策

#回答関数
def Answer():
    print(f"ボールがある場所を入力してください(ボール:{len(balls_ans)}個 不同順OK)")
    print("入力は[x,y]の形で入力してください(左上角を1,1とします)")
    print("入力例:1,1 2,2 3,3 4,4 5,5")
    while True:
        try:
            ans = [[int(b) for b in a.split(",")] for a in input(":").split()]
            for i in ans:
                try:
                    if i[0] < 1 or i[0] > 8 or i[1] < 1 or i[1] > 8:
                        print("1~8の整数を入力してください")
                        break
                except IndexError:
                    print("入力エラーです 再入力してください")
                    break
            else:
                break
        except ValueError:
            print("入力エラーです 再入力してください")
    #順番違い防止のための並べ替え
    ans.sort()
    balls_ans.sort()
    #合っているか確認
    print("")
    if ans == balls_ans:
        print("  +---------+\n  |  正解!! |\n  +---------+")
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
    continued = SetNumber()
    if continued == 1:
        Move()
        count += 1
    elif continued == 0:
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
