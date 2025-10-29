# 带可变参数的装饰器使用


def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("老铁，新加的代码6666")
        return func(*args, **kwargs)

    return wrapper


@my_decorator
def my_sum(*args, **kwargs):
    '''
    :param args: 参数列表
    :param kwargs: 参数字典
    :return: 参数的结果求和
    '''

    sum = 0
    # 方法一：遍历求和
    for i in args:
        sum += i

    for i in kwargs.values():
        sum += i

    return sum


# 执行测试案例
res = my_sum(1, 2, 3, 4, a=4, b=5, c=6, d=7)
print(res)
