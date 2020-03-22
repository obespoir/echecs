# coding=utf-8

__author__ = 'jamon'

from service.room.models.roomdesk_manager import desk_mgr
from service.mahjong.controls.gamemanager import game_manager


class BridgeController(object):
    """
    房间和游戏交互接口
    """
    def __init__(self):
        pass

    def start_game(self, desk_id, custom_config=None):
        """
        房间通知游戏内游戏开始
        :param desk_id:
        :param custom_config: None代表默认使用上一局的配置
        :return:
        """
        return game_manager.start_game(desk_id, custom_config=custom_config)

    def player_act(self, desk_id, seat_id, act_type, act_params):
        """
        房间传递过来的玩家操作（过/吃/碰/胡/杠）
        :param seat_id: 桌子号
        :param seat_id: 座位序号
        :param act_type: 操作类型
        :param act_params: 操作参数, json串
        :return:
        """
        return game_manager.player_act(desk_id, seat_id, act_type, act_params)

    def end_desk(self, desk_id):
        """
        桌子解散
        :param desk_id:
        :return:
        """
        return game_manager.del_game_desk(desk_id)

    def get_reconnect_desk_info(self, desk_id, seat_id):
        """
        获取断线重连时的游戏信息
        :param desk_id:
        :param seat_id:
        :return:
        """
        return game_manager.get_reconnect_desk_info(desk_id, seat_id)

    def user_test_act(self, desk_id, seat_id, act, card_list):
        """
        获取断线重连时的游戏信息
        :param desk_id:
        :param seat_id:
        :return:
        """
        return game_manager.test_act(desk_id, seat_id, act, card_list)

    def notify_player(self, desk_id, seat_id, command_id, data, code=200):
        """
        通知桌子上的单个玩家
        """
        desk_mgr.notify_player(desk_id, seat_id, command_id, data, code)

    def notify_desk(self, desk_id, command_id, data):
        """
        通知桌子上的所有玩家
        """
        desk_mgr.notify_desk(desk_id, command_id, data)

    def notify_desk_game_over(self, desk_id):
        """
        通知桌子游戏结束用于改变桌子状态
        """
        desk_mgr.notify_desk_game_over(desk_id)

    def notify_settle_data(self, desk_id, data):
        """
        游戏通知桌子，给予结算数据
        :param desk_id:
        :param data:
        :return:
        """
        desk_mgr.notify_settle_data(desk_id, data)


bridge_controller_ins = BridgeController()