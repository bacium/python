"""
    算法计数:有a,b,c三个数,a+b+c=1000
    a**2+b**2=c**2
    求三数分别是多少,并记录实现时间

"""
import time


# 实现1:
def func1():
    start = time.time()
    for a in range(1, 1001):
        for b in range(1, 1001):
            for c in range(1, 1001):
                if a ** 2 + b ** 2 == c ** 2 and a + b + c == 1000:
                    print(a, b, c)

    end = time.time()
    print(f"实现时间是{end - start}秒")  # 实现时间是145.1968550682068秒


# 实现2
def func2():
    start = time.time()
    for a in range(1, 1001):
        for b in range(1, 1001):
            for c in range(1, 1001):
                if a + b + c == 1000 and a ** 2 + b ** 2 == c ** 2:
                    print(a, b, c)

    end = time.time()
    print(f"实现时间是{end - start}秒")  # 实现时间是95.49515771865845秒


# 实现3
def func3():
    start = time.time()
    for a in range(1, 1001):
        for b in range(1, 1001):
            c = 1000 - a - b
            if a ** 2 + b ** 2 == c ** 2:
                print(a, b, c)

    end = time.time()
    print(f"实现时间是{end - start}秒")  # 实现时间是0.2322239875793457秒


"""
    结论:分别调用func函数,看计算结果用的时间差距明显,func1所用时间最大,func3所用时间最短
"""
