# coding=utf-8
import os

import redis

from ..config_parser import ConfigParser

"""
redis 相关
"""
path = os.getcwd() + "/config.ini"
print("redis_utils", path)
settings = ConfigParser(path)
redis_db = redis.Redis.from_url(settings.get("REDIS_URL"))

def init_redis_db(host="127.0.0.1", port=6379, db=0, password=None):
    redis_db = redis.Redis(host, port, db, password)
    print(u"开始连击redis 获取实例=", redis_db)
    print(redis_db.ping())
    return redis_db


def init_redis_db_from_url(url):
    redis_db = redis.Redis.from_url(url)
    print(u"开始连击redis from_url 获取实例=", redis_db)
    return redis_db


def init_redis_db_with_out_flask(url):
    redis_db = redis.Redis.from_url(url)
    return redis_db


if __name__ == "__main__":
    r = init_redis_db(host="119.23.66.138", port=25012, db=10, password="123456")

    print(r.ping())
