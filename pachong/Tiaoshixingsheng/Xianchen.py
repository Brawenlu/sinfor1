# -*- coding: utf-8 -*-
# @Time    : 2019/12/3 11:11
# @Author  : LWB
# @FileName: Xianchen.py
# @Software: PyCharm
import threading
import queue as Queue
event = threading.Event()
class MyTread(threading.Thread):

    def __init__(self, thread_name, q):
        super().__init__()
        self.name = thread_name
        self.q = q

    def run(self):
        print("开始线程{}".format(self.name))
        while True:
            try:
                user, sleep_time, sku_name = self.q.get(timeout=1)
                if not self.q.qsize():
                    event.set()  # 当队列全部被取完的时候，放行全部的线程
                event.wait()
                # user = User(username=user, sleep_time=sleep_time)
                # user.to_buy_sku(sku_name_list=sku_name)
            except Queue.Empty:
                break
            except Exception as ex:
                print("线程 {} 发生未知错误 错误信息为{}".format(threading.current_thread().getName(), ex))
        print("线程{}结束了".format(threading.current_thread().getName()))
def main():
    # 批量设置用户，对应购买的商品，默认秒杀时间=当天的早上十点--所有用户必须是湖南区域，如果不是 需要在每个线程去获取真实的秒杀时间
    user_dict = {
        '陆文博&0.75': ["大渔印象 免浆黑鱼片 250g/盒 正负25g"],
        # '彭敏&0.72': ["海信 液晶电视 1台 65寸 195W"],
        # '彭敏小号&0.8': ["海信 液晶电视 1台 65寸 195W"]
        # '彭敏小号&0.77': ["Apple iPhone11手机 1台 128GB 黄色 双卡双待"],
        # '曾元明一号&0.76': ["Apple iPhone11手机 1台 128GB 黄色 双卡双待"],
        # '曾元明二号&0.75': ["Apple iPhone11手机 1台 128GB 黄色 双卡双待"],

    }
    workqueue = Queue.Queue(len(user_dict))
    thread_num = len(user_dict)  # 线程数等于用户数
    thread_name_list = [str(i) + str(j) for i, j in zip(["线程"] * thread_num, list(range(1, thread_num + 1)))]
    threads = []
    # 将用户和需要购买的商品填充到队列，同时创建线程
    for user, sku_name in user_dict.items():
        workqueue.put([user.split("&")[0], user.split("&")[1], sku_name])

    for threadname in thread_name_list:
        thread = MyTread(threadname, workqueue)
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()