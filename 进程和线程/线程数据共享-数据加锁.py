# 线程之间数据共享

import threading

global_num = 0

# 添加线程锁，被锁的线程执行完释放资源后其他线程才可以进行数据处理，不然会出现同时操作数据的问题，造成程序异常
"""
    1、使用线程锁应注意上锁的代码在运行任务结束必须及时释放线程锁，否则会出现死锁情况。
    2、上锁时应使用相同锁对数据进行封闭上锁处理，使用不同锁，起不到数据分开处理的效果。
"""
mutex = threading.Lock()


def thread_func1():
    mutex.acquire()
    global global_num
    for i in range(1000000):
        global_num += 1
    print(f"线程1计算后的全局变量：{global_num}")
    mutex.release()


def thread_func2():
    mutex.acquire()
    global global_num
    for i in range(1000000):
        global_num += 1
    print(f"线程2计算后的全局变量：{global_num}")
    mutex.release()


if __name__ == '__main__':
    t1 = threading.Thread(target=thread_func1)
    t2 = threading.Thread(target=thread_func2)
    t1.start()
    t2.start()
