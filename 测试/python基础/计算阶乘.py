# 使用while计算阶乘


# result = 1
# num = 5
# while num > 1:
#     result *= num
#     num -= 1
#
# print(result)

def get_result(n):
    result = 1
    num = n
    while num > 1:
        result *= num
        num -= 1
    return result


print(get_result(6))
