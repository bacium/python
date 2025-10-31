def func(a, b):
    return a + b


# 带参数的lambda表达式
func1 = lambda a, b: a + b
# print(func1(10,20))
# print(func(1,2))


# 带默认参数的lambda表达式

func2 = lambda a, b, c=100: a + b + c
print(func2(100, 200))
