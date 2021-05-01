#!/usr/bin/env python
# coding: utf-8
"""
@author   ChenDehua 2021/5/1 11:04
@note     
"""
import socket
from socketwrapper import SocketWrapper
from base.eventloop import EventLoop


class TCPServer:

    def __init__(self, loop):
        self.loop = loop
        self.loop.add_coroutine(self.run_server_forever())
        # create socket
        s = socket.socket()
        s.bind(("127.0.0.1", 8999))
        s.listen()
        self.listen_socket = SocketWrapper(s, loop)

    async def handler_client(self, socket):
        while True:
            data = await socket.recv(1024)
            if not data:
                print("client disconnected")
                break
            await socket.send(data.upper())

    async def run_server_forever(self):
        while True:
            # 如果accept成功了 直接return返回到这里
            # 如果没有连接 await一个可等待对象，往epoll注册事件 让出CPU 让epoll负责非阻塞异步就绪通知
            socket, addr = await self.listen_socket.accpet()
            print("connected : {}".format(addr))
            self.loop.add_coroutine(self.handler_client(socket))


if __name__ == "__main__":
    try:
        loop = EventLoop()
        server = TCPServer(loop)
        loop.run_forever()
        print("=====")
    finally:
        loop.close()
