# coding=utf-8
import datetime
import time

"""
时间处理工具
"""


def util_get_start_end_time_by_date(time_str, to_time_str=None, format='%m/%d/%Y'):
    """
    此方法用于将当日日期(默认字符串类型 "%m/%d/%Y" )分解成 0:00:01 ~ 23:59:59  两个时间戳
    :param time_str: 字符串类型的时间 例如:1/3/2017
    :param format: 字符串类型时间的格式 例如:'%m/%d/%Y'
    :return: 当日开始毫秒,当日结束毫秒
    """
    if not to_time_str:
        to_time_str = time_str
    start_datetime = datetime.datetime.strptime(time_str, format)  # 将字符串日期格式为 date格式 2017-01-03 00:00:00
    start_time = time.mktime(start_datetime.timetuple())  # 将date格式 转化为 时间戳 1483372800.0
    end_datetime = datetime.datetime.strptime(to_time_str, format)
    end_time = time.mktime(end_datetime.timetuple()) + 24 * 60 * 60 - 1
    if start_time > end_time:
        return end_time, start_time
    return start_time, end_time


def change_time_to_date(time_str, format='%m/%d/%Y'):
    """
    此方法用于将当日日期(默认字符串类型 "%m/%d/%Y" )转化为时间戳
    :param time_str: 字符串类型的时间 例如:1/3/2017
    :param format: 字符串类型时间的格式 例如:'%m/%d/%Y'
    :return: 当日开始毫秒
    """
    start_datetime = datetime.datetime.strptime(time_str, format)  # 将字符串日期格式为 date格式 2017-01-03 00:00:00
    start_time = time.mktime(start_datetime.timetuple())  # 将date格式 转化为 时间戳 1483372800.0
    return start_time


def change_end_time_to_date(time_str, format='%m/%d/%Y'):
    """
    此方法用于将当日日期(默认字符串类型 "%m/%d/%Y" )转化为当日最后一秒时间戳
    :param time_str: 字符串类型的时间 例如:1/3/2017
    :param format: 字符串类型时间的格式 例如:'%m/%d/%Y'
    :return: 当日结束毫秒
    """
    start_datetime = datetime.datetime.strptime(time_str, format)  # 将字符串日期格式为 date格式 2017-01-03 00:00:00
    start_time = time.mktime(start_datetime.timetuple())  # 将date格式 转化为 时间戳 1483372800.0
    end_time = start_time + 24 * 60 * 60 - 1
    return end_time
