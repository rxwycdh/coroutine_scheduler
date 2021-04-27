#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2021/4/27 12:10
@note     
"""
from loop import coroutine, YieldLoop
from collections import deque
import random
import string
import time


# 求等差数列
@coroutine
def test1():
    sum = 0
    for i in range(1, 11):
        if i % 2 == 1:
            sum += yield i
    print("sum = {}".format(sum))


# 生产者-消费者模型
@coroutine
def producer(queue):
    while True:
        good = "".join(random.sample(string.ascii_letters + string.digits, 8))
        queue.append(good)
        cnt = len(queue)
        print("producer produce good, cnt = {}".format(cnt))
        if cnt:
            yield


@coroutine
def consumer(queue):
    while True:
        while len(queue) <= 0:
            print("queue is empty")
            yield
        good = queue.popleft()
        print("consumer consum good {}, cnt {}".format(good, len(queue)))
        time.sleep(1)


if __name__ == "__main__":
    # YieldLoop.instance().add_coroutine(test1())
    # YieldLoop.instance().run_until_complete()

    q = deque()
    YieldLoop.instance().add_coroutine(producer(q))
    YieldLoop.instance().add_coroutine(producer(q))
    YieldLoop.instance().add_coroutine(producer(q))
    YieldLoop.instance().add_coroutine(consumer(q))
    YieldLoop.instance().run_until_complete()
