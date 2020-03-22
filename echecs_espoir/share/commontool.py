# coding:utf-8

'''
author: jamon
'''

import hashlib
import random
import time
import ujson
from functools import wraps

from obespoir.share.ob_log import logger

MAX_EXCEED_TIME = 10


def get_md5(content):
    c_md5 = hashlib.md5()
    c_md5.update(content)
    return c_md5.hexdigest()


def record_spent_time(filename):
    """
    每个handler请求时间的装饰器
    :param filename:
    :return:
    """

    def record_spent(func):
        @wraps(func)
        def handler_func(*args, **kwargs):
            start_time = time.time()
            logger.info("start " + str(filename) + " time: " + str(start_time))

            res = func(*args, **kwargs)

            end_time = time.time()
            logger.info("end " + str(filename) + " time: " + str(end_time))

            spent_time = end_time - start_time
            if spent_time > MAX_EXCEED_TIME:
                logger.warning("handler " + str(filename) + " spent time: " + str(spent_time) + ",exceed time!")
            else:
                logger.info("handler " + str(filename) + " spent time: " + str(spent_time) + ",ok.")
            return res

        return handler_func

    return record_spent


def weight_choice(weight):
    """
    :param weight: list对应的权重序列
    :return:选取的值在原列表里的索引
    """
    t = random.randint(0, sum(weight) - 1)
    for i, val in enumerate(weight):
        t -= val
        if t < 0:
            return i


def convert_to_json(data):
    if isinstance(data, dict):
        return data

    if isinstance(data, str):
        return ujson.loads(data)

    return {}
