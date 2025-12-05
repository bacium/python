# 装饰器-多个装饰器装饰一个函数


def my_decorator(func):
    def inner(x, y):
        if func.__name__ == 'get_sum':
            print("玩命累加中……")
        else:
            print("递减中……")
        return func(x, y)

    return inner


@my_decorator
def get_sum(a, b):
    return a + b


@my_decorator
def get_sub(a, b):
    return a - b


# print(get_sum(1, 2))
print(get_sub(10, 5))
