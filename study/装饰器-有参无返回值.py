# 有参无返回值装饰器


def my_decorator(func):
    def inner(x, y):
        print("其他操作……")
        func(x, y)

    return inner


def my_sum(a, b):
    print(a + b)


print("======================传统写法======================")
my_sum = my_decorator(my_sum)
my_sum(1, 2)

print("======================使用装饰器======================")


@my_decorator
def my_sum(a, b):
    print(a + b)


my_sum(10, 20)
