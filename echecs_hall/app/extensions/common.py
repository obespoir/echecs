#!/usr/bin/env python
# coding=utf-8
import hashlib
import time
import datetime


# md5加密
def md5(param):
    m = hashlib.md5()
    m.update(param)
    return m.hexdigest()


def diff_days(timestamp):
    now = time.time()
    t1 = time.strftime('%Y-%m-%d', time.localtime(now))
    t2 = time.strftime('%Y-%m-%d', time.localtime(timestamp))
    a_ = datetime.datetime.strptime(t1, '%Y-%m-%d')
    b_ = datetime.datetime.strptime(t2, '%Y-%m-%d')
    return (a_ - b_).days


def diff_hours(timestamp):
    t1 = float(time.time())
    t2 = float(timestamp)
    hour = (t1 - t2) / 3600
    return hour




