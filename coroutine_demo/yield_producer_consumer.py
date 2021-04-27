#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2021/4/26 21:34
@note     
"""
import time


def consumer(cnt):
    gen = producer()
    next(gen)
    cnt = gen.send(cnt)
    while True:
        cnt -= 1
        if cnt <= 0:
            print("consumer consumer , cnt = {}".format(cnt))
            cnt = gen.send(cnt)
        time.sleep(1)


def producer():
    cnt = yield
    while True:
        cnt = yield cnt
        cnt += 1
        print("producer producer, cnt = {}".format(cnt))


def func(n):
    sum = 0
    for i in range(1, n + 1):
        sum += yield i
    print("sum = {}".format(sum))


if __name__ == "__main__":
    consumer(1)
    # for i in func(10):
    #     print(i)
