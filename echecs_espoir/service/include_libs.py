# coding=utf-8
"""
author = jamon
"""

from service import http_handler, rpc_handler, ws_handler


"""初始化游戏内部需要的库"""
import service.room
import service.mahjong.models.config.init_config