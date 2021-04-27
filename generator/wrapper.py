#!/usr/bin/env python
# coding: utf-8
"""
生成器协程适配器
重写生成器方法：send,next(生成器通过这两个函数进行调度的，重写使他能在调度器里面执行)
@author   ChenDehua 2021/4/27 10:48
@note     
"""


class CoroutineWrapper:

    def __init__(self, loop, generator):
        # 调度器
        self.loop = loop
        # 生成器
        self.generator = generator
        # 生成器上下文
        self.context = None

    def send(self, val):
        # 调用生成器原本的send方法
        val = self.generator.send(val)  # 第一次send(None) val 变为1
        self.context = val
        self.loop.add_runnables(self)

    def throw(self, tp, *rest):
        # 向生成器上次yield挂起的位置抛出一个异常
        return self.generator.throw(tp, *rest)

    def close(self):
        return self.generator.close()

    def __next__(self):
        val = next(self.generator)
        self.context = val

    def __getattr(self, name):
        return getattr(self.generator, name)

    def __str__(self):
        return "coroutine-wrapper : {} context {}".format(self.generator, self.context)
