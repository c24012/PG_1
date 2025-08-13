import random
count = [0] * 6
for i in range(100):
    count[random.randint(0,5)] += 1
for i in range(6):
    print(f"{i+1}:{"*"*count[i]}")

