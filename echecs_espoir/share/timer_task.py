# coding=utf-8

import asyncio
from obespoir.base.global_object import GlobalObject


class TimerTask(object):
    @classmethod
    def call_later(cls, interval, callback_func, *args, **kwargs):
        return asyncio.ensure_future(cls.run(interval, callback_func, *args, **kwargs), loop=GlobalObject().loop)
        # return reactor.callLater(interval, callback_func, *args, **kwargs)

    @classmethod
    async def run(cls, interval, callback_func, *args, **kwargs):
        await asyncio.sleep(interval)
        callback_func(*args, **kwargs)


