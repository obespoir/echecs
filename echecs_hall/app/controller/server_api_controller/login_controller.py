# coding=utf-8
from app.data_bridge import er_mj_bridge


def validate_user_in_redis(user_id):
    """
    通过用户名密码验证该用户是否登录
    :param user_id:
    :return:
    """
    # TODO 查看是否在redis中
    r = er_mj_bridge.get_user_by_user_id(user_id)
    return bool(r)


def validate_user_password(user_id, pwd):
    """
    验证用户密码是否正确
    :param user_id:
    :param pwd:
    :return: bool
    """
    # TODO 验证密码
    ret = er_mj_bridge.validate_user_password(user_id, pwd)
    return ret


def get_room_name(user_id):
    """
    根据策略获取一个房间名用于客户端链接服务器
    :param user_id:
    :return:
    """
    return "room_1"


def is_login(session_id):
    """
    判断用户是否登录
    :param session_id:
    :return:
    """
    return er_mj_bridge.is_login(session_id)


def notify_prev_user(session_id=None):
    """
    通知被抢登玩家
    :param session_id:
    :return:
    """
    # TODO 代用推送接口 通知玩家
    er_mj_bridge.notify_prev_user(session_id)
    pass


def exist_user_desk(user_id):
    """
    查询用户是否在桌子中,借此判断是否需要断线重连
    :param user_id:
    :return:
    """
    # TODO 查看用户是否在桌子中
    return er_mj_bridge.exist_user_desk(user_id)


def enter_game(user_id, session_id, room_name):
    """
    用户登录成功,则进入游戏,需要将用户session 和 user_id 对应 写入 redis 已被查询
    :param user_id:
    :param session_id:
    :return:
    """

    return er_mj_bridge.enter_game(user_id, session_id, room_name)