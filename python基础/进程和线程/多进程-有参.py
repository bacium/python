# 多进程带参数的运行实现
import multiprocessing
import time


def coding(name, num):
    for i in range(1, num + 1):
        time.sleep(0.1)
        print(f"{name}在编码路上越走越远的第{i}遍")


def music(name, count):
    for i in range(1, count + 1):
        time.sleep(0.1)
        print(f"******{name}上班给的叫工资，摸鱼{i}遍才是赚钱********")


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=coding, args=("张三", 10))
    p2 = multiprocessing.Process(target=music, kwargs={"count": 12, "name": "李四"})
    p1.start()
    p2.start()
