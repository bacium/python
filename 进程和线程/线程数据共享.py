# 线程之间数据共享

import threading

global_num = 0


def thread_func1():
    global global_num
    for i in range(1000000):
        global_num += 1
    print(f"线程1计算后的全局变量：{global_num}")


def thread_func2():
    global global_num
    for i in range(1000000):
        global_num += 1
    print(f"线程2计算后的全局变量：{global_num}")


if __name__ == '__main__':
    t1 = threading.Thread(target=thread_func1)
    t2 = threading.Thread(target=thread_func2)
    t1.start()
    t2.start()
