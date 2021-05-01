#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2021/5/1 10:26
@note     
"""
import select


class SocketWrapper:

    def __init__(self, socket, loop):
        socket.setblocking(False)
        self.loop = loop
        self.socket = socket

    def fileno(self):
        return self.socket.fileno()

    def create_future_for_event(self, event):
        future = self.loop.create_future()

        def handler():
            future.set_done()
            self.loop.unregister_handler(self.fileno())
            if future.coroutine:
                # 保持future关注的协程继续调度 因为是socket
                self.loop.add_coroutine(future.coroutine)

        # 往epoll注册此future的事件用于监听
        self.loop.register_handler(self.fileno(), event, handler)
        return future

    # ---- wrap the socket blocking method

    async def accpet(self):
        while True:
            try:
                socket, addr = self.socket.accept()
                return SocketWrapper(socket, self.loop), addr
            except BlockingIOError:
                future = self.create_future_for_event(select.EPOLLIN)
                await future

    async def recv(self, size):
        while True:
            try:
                return self.socket.recv(size)
            except BlockingIOError:
                future = self.create_future_for_event(select.EPOLLIN)
                await future

    async def send(self, data):
        while True:
            try:
                return self.socket.send(data)
            except BlockingIOError:
                future = self.create_future_for_event(select.EPOLLOUT)
                await future
