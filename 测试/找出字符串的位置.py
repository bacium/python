str1 = "helloworldhellopythonhelloc++hellojava"

# 找出字符串包含所有hello的下标,并返回一个元组
def findal1(main_string, sub_string):
    positions = []
    start = 0
    length = len(sub_string)
    while True:
        pos = main_string.find(sub_string, start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + 1

    return tuple(positions)


result = findal1(str1, "hello")
print(result)  # 输出: (0, 10, 21, 29)
