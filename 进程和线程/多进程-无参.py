"""
分别使用两个进程运行两个不同的函数，查看运行状态时两个进程分开执行的过程是不是交替式进行
"""
import multiprocessing
import os
import time


def coding():
    getPid = os.getpid()
    for i in range(10):
        time.sleep(0.1)
        print(f"{getPid}在编码路上越走越远的第{i}遍")


def music():
    getPid = os.getpid()
    for i in range(10):
        time.sleep(0.1)
        print(f"******{getPid}上班给的叫工资，摸鱼{i}遍才是赚钱********")


p1 = multiprocessing.Process(target=coding)
p2 = multiprocessing.Process(target=music)
if __name__ == '__main__':
    p1.start()
    p2.start()
