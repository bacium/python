# 无参有返回值装饰器

def my_decorator(func):
    def wrapper():
        print("other code ……")
        return func()  # 注意：有返回值则要返回函数调用的结果，必须将结果返回，否则外部无法获取到函数执行结果

    return wrapper


print("==================传统写法================")


# 定义原函数
def my_sum():
    a = 10
    b = 20
    return a + b


my_sum = my_decorator(my_sum)
result = my_sum()
print(result)

print("==================使用装饰器================")


@my_decorator
def my_sum():
    a = 10
    b = 50
    return a + b


result = my_sum()
print(result)
