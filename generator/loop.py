#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2021/4/27 10:35
@note     
"""
import functools
from collections import deque
from wrapper import CoroutineWrapper
import inspect


def coroutine(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        # 判断func是不是一个生成器
        if inspect.isgenerator(gen):
            coro = CoroutineWrapper(YieldLoop.instance(), gen)
            return coro
        else:
            raise RuntimeError("function is not supported ,require generator,type:{}".format(type(gen)))

    return wrapper


class YieldLoop:
    current = None

    runnables = deque()

    @classmethod
    def instance(cls):
        return YieldLoop.current or YieldLoop()

    def add_coroutine(self, coro):
        assert isinstance(coro, CoroutineWrapper), 'coro is not CoroutineWrapper type!'
        self.add_runnables(coro)

    # 执行协程
    def run_coroutine(self, coro):
        try:
            # 从协程的上下文context中取出context值，然后send过去，（其实就是将上次yield的返回结果保存起来到context
            # 然后这里再send去协程(协程可能就有类似于sum += yiled i这样的语句，因为保存了上下文 所以就变成 sum += coro.context)
            # 解决像 cnt = yield i print(cnt)为None的情况
            # print("run coro :", coro)
            coro.send(coro.context)
        except StopIteration as e:
            print("coroutine {} stop".format(coro))

    def run_until_complete(self):
        while YieldLoop.runnables:
            # print("runnables:", YieldLoop.runnables)
            coro = YieldLoop.runnables.popleft()
            self.run_coroutine(coro)

    def add_runnables(self, coro):
        self.runnables.append(coro)
