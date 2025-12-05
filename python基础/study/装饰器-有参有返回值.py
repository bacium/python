# 有参有返回值装饰器

def my_decorator(func):
    def wrapper(x, y):
        print("other code ……")
        return func(x, y)

    return wrapper


def my_sum(a, b):
    return a + b


print("==========================传统写法==========================")

my_sum = my_decorator(my_sum)
result = my_sum(1, 2)
print(result)

print("==========================使用装饰器==========================")


@my_decorator
def my_sum(a, b):
    return a + b


result = my_sum(1, 90)
print(result)
