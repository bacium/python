"""
分别使用两个线程运行两个不同的函数，查看运行状态时两个线程分开执行的过程是不是交替式进行
"""
import threading
import time


def coding():
    for i in range(10):
        time.sleep(0.1)
        print(f"在编码路上越走越远的第{i}遍")


def music():
    for i in range(10):
        time.sleep(0.1)
        print(f"******上班给的叫工资，摸鱼{i}遍才是赚钱********")


t1 = threading.Thread(target=coding)
t2 = threading.Thread(target=music)
if __name__ == '__main__':
    t1.start()
    t2.start()
