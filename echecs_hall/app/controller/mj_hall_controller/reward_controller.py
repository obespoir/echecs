# coding=utf-8
from app.data_bridge import mj_hall_bridge


def get_all_reward_info():
    """
    获取奖励详情
    :param:
    :return:list
    """
    return mj_hall_bridge.get_all_reward_info()