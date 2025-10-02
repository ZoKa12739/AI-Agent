import threading
import time

# 全局变量，将被两个线程互斥访问
count = 0
# 创建互斥锁
lock = threading.Lock()

# 线程函数1
def thread_function_1():
    global count
    for _ in range(5):
        # 获取锁，进入临界区
        lock.acquire()

        # 临界区代码 - 互斥访问count
        count += 1
        print(f"线程1: count = {count}")

        # 释放锁，退出临界区
        lock.release()

        # 短暂休眠，让另一个线程有机会执行
        time.sleep(0.1)

# 线程函数2
def thread_function_2():
    global count
    for _ in range(5):
        # 获取锁，进入临界区
        lock.acquire()

        # 临界区代码 - 互斥访问count
        count += 1
        print(f"线程2: count = {count}")

        # 释放锁，退出临界区
        lock.release()

        # 短暂休眠，让另一个线程有机会执行
        time.sleep(0.1)

if __name__ == "__main__":
    # 创建两个子线程
    thread1 = threading.Thread(target=thread_function_1)
    thread2 = threading.Thread(target=thread_function_2)

    # 启动线程
    thread1.start()
    thread2.start()

    # 等待两个线程执行完毕
    thread1.join()
    thread2.join()

    print(f"主线程完成，最终count值: {count}")