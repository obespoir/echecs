# coding=utf-8

from service.mahjong.constants.gamedefine import Act
from config.globalconfig import GlobalConfig
from service.mahjong.models.utils.notify_playeract import notify_player_ins


class BaseSystemAct(object):
    """基础麻将系统操作"""
    def __init__(self, game_data):
        self.game_data = game_data

    @property
    def desk_id(self):
        return self.game_data.desk_id

    @property
    def players(self):
        return self.game_data.players

    @property
    def max_player_num(self):
        return self.game_data.max_player_num

    @property
    def game_config(self):
        return self.game_data.game_config

    @property
    def card_dealer(self):
        return self.game_data.card_dealer

    @property
    def card_analyse(self):
        return self.game_data.card_analyse

    @property
    def banker_seat_id(self):
        return self.game_data.banker_seat_id

    def get_next_seat_id(self, seat_id):
        return self.game_data.get_next_seat_id(seat_id)

    def get_act_wait_time(self, seat_id, act_type=Act.CHU):
        if self.game_data.is_player_auto(seat_id):
            return GlobalConfig().auto_op_wait_time
        elif self.game_data.players[seat_id].hand_card.is_ting and act_type not in [Act.AN_GANG, Act.ZI_MO, Act.BU_GANG]:
            return GlobalConfig().ting_auto_chu_time
        else:
            if act_type in [Act.CHI, Act.PENG, Act.DIAN_GANG, Act.DIAN_HU]:
                return GlobalConfig().manual_op_against_act_time
            elif act_type in [Act.WAITE_ANSWER]:
                return GlobalConfig().waite_answer_time
            else:
                return GlobalConfig().manual_op_wait_time


    def notify_player_to_act(self, seat_id, act_info={}, interval=1000):
        """
        通知玩家进行操作
        :param seat_id:
        :param act_info:  {act_type:params}
        :param interval:
        :return:
        """
        return notify_player_ins.notify_player(self.desk_id, seat_id, act_info=act_info, interval=interval)
