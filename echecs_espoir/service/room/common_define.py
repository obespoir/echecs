# coding=utf-8


class UserStatus(object):
    """用户状态"""
    UNREADY = 1    # 待准备
    READY = 2      # 准备中
    PLAYING = 3    # 游戏中
    ESCAPE = 4     # 逃跑
    OFFLINE = 5    # 离线


class DeskStatus(object):
    """桌子状态"""
    READY = 1
    PLAYING = 2
    OVER = 3


class DeskType(object):
    FRIEND_DESK = 1
    MATCH_DESK = 2