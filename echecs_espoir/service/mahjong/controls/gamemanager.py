# coding=utf-8

__author__ = 'jamon'


class GameManager(object):
    """
    管理不同桌游戏
    """
    def __init__(self):
        self._game_desks = {}

    def add_game_desk(self, game_desk):
        self._game_desks[game_desk.desk_id] = game_desk

    def del_game_desk(self, desk_id):
        self._game_desks.pop(desk_id, None)

    def get_game_desk(self, desk_id):
        return self._game_desks.get(desk_id, None)

    def start_game(self, desk_id, custom_config=None, new_round=False, game_type="default"):
        """
        游戏内游戏开始
        :param desk_id:
        :param custom_config: None代表默认使用上一局的配置
        :param new_round: 是否为新的一轮
        :param game_type: 使用的麻将基本玩法类型
        :return:
        """
        from service.mahjong.controls.gamedesk import GameDesk
        desk = self.get_game_desk(desk_id)
        if new_round:
            if desk:
                self.del_game_desk(desk_id)
            desk = GameDesk(desk_id, custom_config, game_type=game_type)
            game_manager.add_game_desk(desk)
        else:
            if not desk:
                desk = GameDesk(desk_id, custom_config, game_type=game_type)
                game_manager.add_game_desk(desk)
        desk.start_game()
        return 1

    def player_act(self, desk_id, seat_id, act_type, act_params):
        """
        房间传递过来的玩家操作（过/吃/碰/胡/杠）
        :param desk_id: 桌子id
        :param seat_id: 座位序号
        :param act_type: 操作类型
        :param act_params: 操作参数, json串
        :return:
        """
        desk = self.get_game_desk(desk_id)
        if not desk:
            return
        r = desk.handle_player_act(seat_id, act_type, act_params)
        return r

    def get_reconnect_desk_info(self, desk_id, seat_id):
        """
        获取断线重连时的游戏信息
        :param desk_id:
        :param seat_id:
        :return:
        """
        desk = self.get_game_desk(desk_id)
        if not desk:
            return {}
        return desk.get_all_info_of_player(seat_id)

    def test_act(self, desk_id, seat_id, act_type, card_list):
        """
        房间传递过来的玩家测试操作
        :param desk_id: 桌子id
        :param seat_id: 座位序号
        :param act_type: 操作类型
        :param card_list: 操作参数[]
        :return:
        """
        desk = self.get_game_desk(desk_id)
        if not desk:
            return
        desk.handler_test_act(seat_id, act_type, card_list)
        return 1


game_manager = GameManager()