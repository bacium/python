# 多线程带参数的运行实现
import threading
import time


def coding(name, mum):
    for i in range(1, mum + 1):
        time.sleep(0.1)
        print(f"编码第{i}遍……")


def music(name, count):
    for i in range(1, count + 1):
        time.sleep(0.1)
        print(f"听音乐的第{i}首歌==============>")


if __name__ == '__main__':
    t1 = threading.Thread(target=coding, args=("老六", 10))
    t2 = threading.Thread(target=music, kwargs={"count": 10, "name": "曹操"})
    t1.start()
    t2.start()
