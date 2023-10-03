# -*- coding: utf-8 -*-
__author__ = "C418____11 <553515788@qq.com>"
__version__ = "0.1.0"

import asyncio
import html
import json
from threading import Thread
from typing import Union

import websockets


class EventList:
    def __init__(self, unescape: bool = True):
        self.data = []
        self.err = None
        self._auto_unescape = unescape

    @staticmethod
    def _unescape(v):
        return html.unescape(v)

    def append(self, v):
        if self._auto_unescape:
            v = self._unescape(v)
        self.data.append(v)

    def clear(self):
        self.data.clear()

    def pop(self, index=-1):
        return self.data.pop(index)

    def __getattribute__(self, item):
        if object.__getattribute__(self, "err") is not None:
            raise object.__getattribute__(self, "err")
        return object.__getattribute__(self, item)


class RecvEventLoop:
    URL = 'ws://localhost:6700/'

    def __init__(self, event_list: Union[EventList, ...] = None):
        self.event_list = event_list
        if event_list is None:
            self.event_list = EventList()

        self._event_loop = asyncio.new_event_loop()
        self._running = False

    async def get_event_loop(self):
        async with websockets.connect(self.URL) as websocket:
            while self._running:
                data = await websocket.recv()
                self.event_list.append(data)

    def _run_event_loop_thread(self):
        try:
            self._event_loop.run_until_complete(self.get_event_loop())
        except Exception as err:
            self._running = False
            self.event_list.err = err

    def start(self):
        self._running = True

        cls_name = type(self).__name__
        Thread(target=self._run_event_loop_thread, daemon=True, name=f"{cls_name}._run_event_loop_thread").start()

    def stop(self):
        self._running = False
        self._event_loop.stop()

    def is_running(self):
        return self._running


class MessageSender:
    URL = 'ws://localhost:6700/api/'

    @classmethod
    async def _sender(cls, data):
        if not data["params"]["message"]:
            raise ValueError("Attempted to send an empty message")
        async with websockets.connect(cls.URL) as websocket:
            await websocket.send(json.dumps(data))
            return [await websocket.recv(), await websocket.recv()]

    @classmethod
    def group(cls, send_to, message, echo=None):
        if echo is None:
            echo = ''

        data = {
            "action": "send_group_msg",
            "params": {
                "group_id": f"{int(send_to)}",
                "message": f"{message}"
            },
            "echo": f"{echo}"
        }

        return asyncio.run(cls._sender(data))

    @classmethod
    def private(cls, send_to, message, echo=None):
        if echo is None:
            echo = ''

        data = {
            "action": "send_private_msg",
            "params": {
                "user_id": f"{int(send_to)}",
                "message": f"{message}"
            },
            "echo": f"{echo}"
        }

        return asyncio.run(cls._sender(data))


class GetMessage:
    URL = 'ws://localhost:6700/api/'

    @classmethod
    async def _getter(cls, message_id):
        async with websockets.connect(cls.URL) as websocket:
            await websocket.send(json.dumps({"action": "get_msg", "params": {"message_id": f"{int(message_id)}"}}))
            return [await websocket.recv(), await websocket.recv()]

    @classmethod
    def __call__(cls, message_id):
        return asyncio.run(cls._getter(message_id))


get_msg = GetMessage()

__all__ = ("EventList", "RecvEventLoop", "MessageSender", "GetMessage")
