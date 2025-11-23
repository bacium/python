import random

result = []
list1 = ["A", "B", "C", "D", "E", "F", "G", "H"]

for s in list1:
    temp = []
    index = random.randint(0, len(list1) - 1)
    temp.append(list1[index])
    print(temp)
    if len(temp) >= 0:
        pass



print(result)
