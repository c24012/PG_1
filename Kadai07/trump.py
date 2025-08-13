import random

#トランプカードリスト作成
suit = ["クラブ","ハート","ダイヤ","スペード"]
cards = [str(x) for x in range(1,14)] * 4
#スートと数字の間に「の」を入れてくっつける
for i in range(4):
    for j in range(i*13,i*13+13):
        cards[j] = suit[i] + "の" + cards[j]

#シャッフル後、5枚取り出す
random.shuffle(cards)
print("あなたがひいたトランプは、")
for _ in range(5):
    print(cards.pop())
print("です。")
