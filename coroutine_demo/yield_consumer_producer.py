#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2021/4/26 20:54
@note     
"""
import time


def consumer():
    cnt = yield
    while True:
        if cnt <= 0:
            print("lalal")
            cnt = yield cnt
        cnt -= 1
        time.sleep(1)
        print("consumer consume 1 cnt cnt = {}".format(cnt))


def producer(cnt):
    gen = consumer()
    next(gen)
    gen.send(cnt)
    print("producer go on ")
    while True:
        cnt += 5
        print("producer produce 5 cnt cnt = {}".format(cnt))
        cnt = gen.send(cnt)
        print("producer cnt :{}".format(cnt))


if __name__ == "__main__":
    producer(0)
