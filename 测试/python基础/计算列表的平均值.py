def average(list):
    # 总和
    sum = 0
    for i in list:
        sum += i
    # 平均值
    result = sum / len(list)
    return result


print(average([1, 2, 3, 8, 9]))
