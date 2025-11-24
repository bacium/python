import random
list1 = ["A", "B", "C", "D", "E", "F", "G", "H"]

# 生成8个随机下标
randomList = []
while len(set(randomList)) < 8:
    randomItem = random.randint(0, 7)
    randomList.append(randomItem)
# print(randomList)

# 注意:此时的 randomList是带有重复的索引值,但是去重后肯定是8个值
selfList = []
for i in randomList:
    if i not in selfList:
        selfList.append(i)
print(selfList)  # 此时的selfList中含有0-7的随机索引,且无重复值
offices = []
temp = []
for i in selfList:
    temp.append(list1[i])
    if len(temp) > 2:
        offices.append(temp)
        temp = []
offices.append(temp)
print(offices)
