import threading
import random
import time

# 缓冲区数量
BUFFER_NUM = 5
# 生产者、消费者数量
PRODUCER_NUM = 2
CONSUMER_NUM = 3
# 缓冲区
buffer = [None] * BUFFER_NUM
# 条件变量，用于协调生产者和消费者
cond = threading.Condition()
# 记录缓冲区使用情况，True 表示已占用，False 表示空闲
buffer_used = [False] * BUFFER_NUM


class Producer(threading.Thread):
    def __init__(self, producer_id):
        super().__init__()
        self.producer_id = producer_id

    def run(self):
        global buffer, buffer_used
        while True:
            with cond:
                # 找到一个空闲缓冲区
                empty_idx = None
                for i in range(BUFFER_NUM):
                    if not buffer_used[i]:
                        empty_idx = i
                        break
                if empty_idx is None:
                    # 没有空闲缓冲区，等待
                    cond.wait()
                    continue
                # 生产物品（这里简单用随机数模拟，也可按规律生成与示例匹配数据 ）
                item = random.randint(0, 100)
                # 放入缓冲区
                buffer[empty_idx] = item
                buffer_used[empty_idx] = True
                print(f"生产者 {self.producer_id} 将物品 {item} 放入缓冲区 [{empty_idx}]")
                # 通知消费者可以消费
                cond.notify_all()
                # 模拟生产间隔
            time.sleep(random.uniform(0.1, 0.5))


class Consumer(threading.Thread):
    def __init__(self, consumer_id):
        super().__init__()
        self.consumer_id = consumer_id

    def run(self):
        global buffer, buffer_used
        while True:
            with cond:
                # 找到一个有物品的缓冲区
                full_idx = None
                for i in range(BUFFER_NUM):
                    if buffer_used[i]:
                        full_idx = i
                        break
                if full_idx is None:
                    # 没有可消费缓冲区，等待
                    cond.wait()
                    continue
                # 取出物品
                item = buffer[full_idx]
                buffer_used[full_idx] = False
                print(f"消费者 {self.consumer_id} 从缓冲区 [{full_idx}] 取出物品 {item}")
                # 通知生产者可以生产
                cond.notify_all()
                # 模拟消费间隔
            time.sleep(random.uniform(0.1, 0.5))


if __name__ == "__main__":
    producers = [Producer(i + 1) for i in range(PRODUCER_NUM)]
    consumers = [Consumer(i + 1) for i in range(CONSUMER_NUM)]

    for p in producers:
        p.start()
    for c in consumers:
        c.start()

    for p in producers:
        p.join()
    for c in consumers:
        c.join()