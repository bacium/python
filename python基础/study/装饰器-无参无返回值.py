# 无参无返回值装饰器

def my_decorator(func):
    def fn_inner():
        print("其他操作……")
        func()

    return fn_inner


def get_sum():
    a = 10
    b = 20
    print(a + b)


print("====================传统写法=====================")
# 传统写法
get_sum = my_decorator(get_sum)
get_sum()

print("====================使用装饰器=====================")


# 使用装饰器
@my_decorator
def get_sum():
    a = 10
    b = 20
    print(a + b)


get_sum()
