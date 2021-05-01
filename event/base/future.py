#!/usr/bin/env python
# coding: utf-8
"""
future:waitable object to await
@author   ChenDehua 2021/5/1 10:27
@note     
"""


class Future:
    def __init__(self, eventLoop):
        self.done = False
        self.eventLoop = eventLoop
        self.coroutine = None

    def set_coroutine(self, coro):
        self.coroutine = coro

    def set_done(self):
        self.done = True

    def __await__(self):
        if not self.done:
            yield self
        return
