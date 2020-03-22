# coding=utf-8
from app.data_bridge import mj_hall_bridge


def get_all_good_info():
    """
    获取全部商品信息
    :param:
    :return:list
    """
    # TODO 获取全部商品信息
    return mj_hall_bridge.get_all_good_info()


def get_good_info_by_id(id):
    """
    根据商品id获取商品信息
    :param:id
    :return:list
    """
    # TODO 根据商品id获取商品信息
    return mj_hall_bridge.get_good_info_by_id(id)