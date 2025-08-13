x = int(input("金額を入力してください:"))
handred = 0
ten = 0
one = 0

if x >= 100:
    handred = x // 100
    x -= handred * 100
if x >= 10:
    ten = x // 10
    x -= ten * 10
    print(x)
if x >= 1:
    one = x

print(f"100円玉{handred}枚,10円玉{ten}枚,1円玉{one}枚")
