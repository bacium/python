# 装饰器的使用

"""
1、闭包方式使用
2、@装饰器名称使用
"""


# def fn_outer(a):
#
#     def fn_inner(b):
#         return a + b
#
#     return fn_inner
#
#
# test_fn = fn_outer(10)(23)
# print(test_fn)

# 方法二

print("+" * 30)


def fn_outer(cb):
    # print("123")

    def fn_inner():
        print("其他操作……………………")
        cb()
        print("其他代码")

    return fn_inner


# 使用装饰器
@fn_outer
def _sum():
    print("a + b")


_sum()
