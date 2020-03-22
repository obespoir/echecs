# coding=utf-8

"""
玩家行为钩子
"""

from service.mahjong.constants.gamedefine import Act
from service.mahjong.models.callbackmanager import CallbackFuncType
from config.globalconfig import GlobalConfig


class PlayerActHook(object):

    def __init__(self, game_data):
        self.game_data = game_data
        self.hook_handler = {           # 行为挂钩的处理函数
            Act.BU_GANG: self.hook_bu_gang,
        }
        self.check_handler = {          # 钩子内部的检查处理
            Act.DIAN_HU: self.can_dian_hu,           # 判断是否可以点炮胡
        }

    @property
    def game_config(self):
        return self.game_data.game_config

    @property
    def players(self):
        return self.game_data.players

    @property
    def max_player_num(self):
        return self.game_data.game_config.max_player_num

    def get_act_wait_time(self, seat_id, act_type=Act.CHU):
        if self.game_data.is_player_auto(seat_id):
            return GlobalConfig().auto_op_wait_time
        else:
            if act_type in [Act.CHI, Act.PENG, Act.DIAN_GANG, Act.DIAN_HU]:
                return GlobalConfig().manual_op_against_act_time
            else:
                return GlobalConfig().manual_op_wait_time

    def hook(self, cur_seat_id, act_type, act_params):
        player_hook = self.game_data.game_config.player_act_hook
        # 玩家行为执行前钩子处理, 如抢杠胡{Act.BU_GANG: [Act.DIAN_HU], ...}
        if act_type not in player_hook.keys():
            return 1
        self.hook_handler.get(act_type)(cur_seat_id, act_type, act_params)

        from service.mahjong.models.utils.notify_playeract import notify_player_ins
        print("hook_check:", self.game_data.cur_players_to_act)
        if self.game_data.cur_players_to_act:
            for i in range(self.max_player_num):
                act_list = self.game_data.get_player_can_speaker(i)
                if act_list:
                    notify_player_ins.notify_player(self.game_data.desk_id, i, act_info=act_list, interval=self.get_act_wait_time(i))
            self.game_data.next_speaker_callback = {"type": CallbackFuncType.FUNC_PLAYER_ACT,
                                                    "call_params": {"seat_id": cur_seat_id, "act_type": act_type,
                                                                    "act_params": act_params}}
            return 0
        else:
            return 1

    def hook_bu_gang(self, cur_seat_id, act_type, act_params):
        params = act_params.get("used_card")
        gang_card_val = params[0]

        for i in range(self.game_config.max_player_num):
            if i == cur_seat_id:
                continue
            self._check(i, cur_seat_id, act_type, gang_card_val)

    def _check(self, seat_id, chu_seat_id, act_type, card_val):
        """

        :param seat_id:  检验玩家的座位号
        :param chu_seat_id: 被检验玩家的座位号（如出牌玩家）
        :param act_type: 被检验玩家的行为类型
        :param card_val: 被检验玩家的行为相关牌
        :return:
        """
        for check in self.game_data.game_config.player_act_hook[act_type]:
            self.check_handler.get(check)(seat_id, chu_seat_id, card_val)

        # 如果玩家可以操作，则添加默认的过操作
        if self.game_data.get_player_can_speaker(seat_id):
            self.game_data.add_player_to_act(seat_id, Act.GUO, act_params={})

        return 1

    def can_dian_hu(self, seat_id, chu_seat_id, card_val):
        hu_result = self.game_data.hu_manager.check_hu_result(self.players[seat_id].hand_card
                                                              , pao_card_val=card_val)
        if hu_result:
            self.game_data.add_player_to_act(seat_id, Act.DIAN_HU,
                                             act_params={"types": hu_result, "hook_seat_id": chu_seat_id})
        return 1
    