def add(a, b):
    return a + b


result = add(10, 34)
print(result)


def sub_(a, b):
    return a - b


print(sub_(10, 34))

# lambda 表达式

add1 = lambda a, b: a + b
print(add1(20, 30))

# 带默认值的lambda表达式


sub1 = lambda a=100, b=30: a - b
print(sub1(18, 2))
