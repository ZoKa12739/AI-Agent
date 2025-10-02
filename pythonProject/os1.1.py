import threading
import time

# 用于线程间通信，通知父线程子线程已完成
event = threading.Event()

def child_thread():
    print("子线程执行")
    # 模拟子线程执行任务耗时
    time.sleep(1)
    print("子线程执行完成")
    # 唤醒父线程
    event.set()
    print("唤醒父线程")

def parent_thread():
    print("父线程执行")
    # 创建并启动子线程
    t = threading.Thread(target=child_thread)
    t.start()
    print("父线程等待子线程完成")
    # 父线程阻塞，直到子线程调用 event.set()
    event.wait()
    print("子线程执行完毕，父线程继续执行")

if __name__ == "__main__":
    print("Hello, This is a Thread.")
    print("hello world")
    print("ThreadA")
    print("ThreadB")
    print("ThreadC")
    parent_thread()
