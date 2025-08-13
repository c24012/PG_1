num_list = [x for x in range(2,101)]
for i in range(100):
    if len(num_list) > i:
        x = num_list[i]
    else:
        break
    for j in reversed(range(len(num_list))):
        if num_list[j] == x:
            continue
        elif num_list[j] % x == 0:
            del num_list[j]

for i in range(len(num_list)):
    if i % 10 == 0 and i != 0:
        print(num_list[i],end=",\n")
    elif i == len(num_list)-1:
        print(num_list[i])
    else:
        print(num_list[i],end=",")
