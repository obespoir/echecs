# coding=utf-8
import copy

from config.globalconfig import GlobalConfig
from service.mahjong.constants.gamedefine import Act, SystemActType
from service.mahjong.models.utils.notify_playeract import notify_player_ins
from service.mahjong.controls.notifybridge import notify_single_user
from service.mahjong.models.timermanager import timer_manager_ins
from service.mahjong.models.callbackmanager import CallbackFuncType
from share.message_ids import PUSH_OTHER_PLAYER_CALL_CARD
from service.mahjong.constants.gamedefine import TimerType


class BasePlayerAct(object):
    """基础麻将玩家操作"""

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
    def card_analyse(self):
        return self.game_data.card_analyse

    @property
    def state_machine(self):
        return self.game_data.state_machine

    def get_next_seat_id(self, seat_id):
        return self.game_data.get_next_seat_id(seat_id)

    def get_act_wait_time(self, seat_id, act_type=Act.CHU):
        if self.game_data.is_player_auto(seat_id):
            return GlobalConfig().auto_op_wait_time
        else:
            if act_type in [Act.CHI, Act.PENG, Act.DIAN_GANG, Act.DIAN_HU]:
                return GlobalConfig().manual_op_against_act_time
            else:
                return GlobalConfig().manual_op_wait_time

    def system_act(self, act_type, act_params={}):
        """
        调用系统操作
        :param act_type:   系统操作类型
        :param act_params: 不同的系统操作类型不同
        :return:
        """
        from service.mahjong.models.systemact.system_act_manager import SystemActManager
        return SystemActManager.get_instance(self.desk_id).system_act(
            act_type=act_type, act_params=act_params)

    def notify_player_to_act(self, seat_id, act_info={}, interval=1000, code=200,t_type=TimerType.NORMAL):
        """
        通知玩家进行操作
        :param seat_id:
        :param act_info:  {act_type:params}
        :param interval:
        :return:
        """
        return notify_player_ins.notify_player(self.desk_id, seat_id, act_info=act_info, interval=interval, code=code,
                                               t_type=t_type)

    def notify_other_player_act_executed(self, seat_id, act_info={}, interval=1000, exclude=[], max_player_num=4):
        """
        通知玩家进行操作
        :param seat_id:
        :param act_info:  {"seat_id": 座位号, "act_type": Act.CHU, "card_list": [操作的牌]}
        :param interval:
        :return:
        """
        return notify_player_ins.notify_some_player(self.desk_id, seat_id, act_info=act_info, interval=interval,
                                                    exclude=exclude, max_player_num=max_player_num)

    def notify_other_player_act_ting(self, seat_id, act_info={}, interval=1000, exclude=[], max_player_num=4):
        """
        通知玩家进行操作
        :param seat_id:
        :param act_info:  {"seat_id": 座位号, "act_type": Act.CHU, "card_list": [操作的牌]}
        :param interval:
        :return:
        """
        return notify_player_ins.notify_some_player_ting(self.desk_id, seat_id, act_info=act_info, interval=interval,
                                                         max_player_num=max_player_num)

    def notify_other_player_act_an_gang(self, seat_id, act_info={}, interval=1000, max_player_num=4):
        """
        通知其他玩家有人进行暗杠操作
        :param seat_id:
        :param act_info:  {"seat_id": 座位号, "act_type": Act.CHU, "card_list": [操作的牌]}
        :param interval:
        :return:
        """
        for i in range(max_player_num):
            is_ting = self.players[i].hand_card.is_ting
            if not i == int(seat_id) and not is_ting:
                tmp_act_info = copy.deepcopy(act_info)
                tmp_act_info["card_list"] = [0]
            else:
                tmp_act_info = act_info
            notify_single_user(self.desk_id, i, PUSH_OTHER_PLAYER_CALL_CARD, tmp_act_info)
            timer_manager_ins.add_timer(self.desk_id, i, interval, call_type=CallbackFuncType.FUNC_AUTO_PLAYER_ACT
                                    , call_params=act_info)
        return 1

    def notify_player_ting(self, seat_id, ting_results):
        """
        通知玩家听
        :param ting_results: {出牌１：{胡的牌:{"fan":胡牌基本类型番数, "type_list":[胡牌类型]}, ...}
        """
        self.game_data.add_player_to_act(seat_id, Act.GUO, act_params={})
        self.game_data.add_player_to_act(seat_id, Act.TING, act_params=ting_results)
        can_op_info = {Act.GUO: {}, Act.TING: ting_results}
        self.players[seat_id].set_can_ting_info(ting_info=ting_results)
        chu_card = self.players[seat_id].hand_card.hand_card_vals[-1]
        self.notify_player_to_act(seat_id, act_info=can_op_info, interval=self.get_act_wait_time(seat_id))
        self.game_data.next_speaker_callback = {"type": CallbackFuncType.FUNC_NOTIFY_PLAYER_ACT, "call_params": {
            "seat_id": seat_id, "interval": self.get_act_wait_time(seat_id, Act.CHU),
            "act_info": {Act.CHU: {"card": chu_card}}}}

    def check_against(self, cur_seat_id, card_val):
        """
        检查其他玩家是否可以操作
        :param cur_seat_id:
        :param card_val:
        :return:
        """
        from service.mahjong.models.systemact.system_act_manager import SystemActManager
        return SystemActManager.get_instance(self.desk_id).system_act(
            act_type=SystemActType.CHECK_AGAINST, act_params={"cur_seat_id": cur_seat_id, "card": card_val})

    def draw_card(self, seat_id, card_num=1, is_last=False):
        """
        玩家摸牌
        :param seat_id:
        :param card_num:
        :param is_last:
        :return:
        """
        from service.mahjong.models.systemact.system_act_manager import SystemActManager
        return SystemActManager.get_instance(self.desk_id).system_act(
            act_type=SystemActType.DRAW_CARD,
            act_params={"seat_id": seat_id, "card_num": card_num, "is_last": is_last})

    def settle(self, settle_type_list=[]):
        """

        """
        from service.mahjong.models.systemact.system_act_manager import SystemActManager
        return SystemActManager.get_instance(self.desk_id).system_act(
            act_type=SystemActType.SETTLE, act_params={"type_list": settle_type_list}
        )

    def end_game(self):
        """

        """
        from service.mahjong.models.systemact.system_act_manager import SystemActManager
        return SystemActManager.get_instance(self.desk_id).system_act(
            act_type=SystemActType.GAME_OVER, act_params={}
        )