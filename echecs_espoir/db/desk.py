# coding=utf-8

from db.redis.desk_pool import DeskPool


class Desk(object):
    def __init__(self):
        pass

    @classmethod
    def get_a_id(cls):
        """
        返回一个随机桌子ID
        :return:
        """
        return DeskPool.pop()

    @classmethod
    def recycle_id(cls, desk_id):
        """
        桌子id回收
        :param desk_id:
        :return:
        """
        return DeskPool.add(desk_id)