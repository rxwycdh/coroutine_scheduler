#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2021/5/1 10:26
@note     
"""
from collections import deque
from select import epoll
from .future import *
import traceback

class EventLoop:

    def __init__(self):
        self.epoll = epoll()
        self.is_stop = False
        self.handlers = {}
        # 不同fileno的回调函数
        self.runnables = deque()

    def create_future(self):
        return Future(self)

    def add_coroutine(self, coro):
        self.runnables.append(coro)

    def run_coroutine(self, coro):
        try:
            # active the coroutine
            future = coro.send(None)
            future.set_coroutine(coro)
        except Exception as e:
            traceback.print_exc()
            print("coroutine {} stopped, exception :{}".format(coro.__name__, e))

    def register_handler(self, fileno, event, handler):
        self.handlers[fileno] = handler
        self.epoll.register(fileno, event)

    def unregister_handler(self, fileno):
        self.handlers.pop(fileno)
        self.epoll.unregister(fileno)

    def run_forever(self):
        while True:
            if self.is_stop:
                break
            while self.runnables:
                self.run_coroutine(self.runnables.popleft())

            events = self.epoll.poll(1)
            for fileno, event in events:
                handler = self.handlers[fileno]
                handler()

        print("eventLoop is stopped")

    def close(self):
        self.is_stop = True
