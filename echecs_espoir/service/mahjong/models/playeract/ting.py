# coding=utf-8

__author__ = 'jamon'
import ujson

from obespoir.share.ob_log import logger
from service.mahjong.models.playeract.base_player_act import BasePlayerAct
from service.mahjong.constants.gamedefine import Act
from service.mahjong.constants.carddefine import BLACK
from service.mahjong.models.actrecord import ActRecord
from service.mahjong.models.timermanager import timer_manager_ins
from service.mahjong.models.callbackmanager import CallbackFuncType
from service.mahjong.models.callbackmanager import CallbackManager
from service.mahjong.constants.gamedefine import TimerType


class Ting(BasePlayerAct):
    def __init__(self, game_data):
        super(Ting, self).__init__(game_data=game_data)
        self.step_handlers = {
            "param_check": self.param_check,                # 参数验证
            "clear_other_act": self.clear_other_act,        # 清除该玩家其他动作
            "set_data": self.set_data,                      # 设置相应数据
            "record": self.record,                          # 记录玩家动作
            "notify_other_player": self.notify_other_player,  # 记录玩家动作
            "clear_lou_hu": self.clear_lou_hu,              # 清除漏胡数据
            "after_ting": self.after_ting                   # 听牌后
        }

        self.chu_card_val = BLACK       # 吃牌使用的牌
        self.cur_ting_card = []         # 目前听的牌
        self.seat_id = -1          # 执行出牌的玩家位置

    def execute(self, act_params={}):
        """
        执行听牌
        :param act_params:
        :return:
        """
        logger.debug(u"听牌: %s", str(act_params))
        for step in self.game_config.player_act_step.get(Act.TING):
            for name, cfg in step.items():
                ret = self.step_handlers.get(name)(act_params=act_params, config_params=cfg)
                if not ret:
                    logger.error("step:%s", step)
                    return
        return 1

    def param_check(self, **kwargs):      # 参数验证
        act_params = kwargs.get("act_params")
        if 1 != len(act_params):
            # 同时只允许有一个玩家发生吃牌操作
            logger.debug(u"act_ting_error:%s", str(act_params))
            return

        seat_id = list(act_params.keys())[0]
        params = act_params[seat_id]

        chu_card = params.get("chu_card")
        if 0 > seat_id or seat_id >= self.max_player_num or chu_card not in self.players[seat_id].can_ting_info.keys():
            logger.error("ting params error: %s", str([seat_id, params]))
            return

        self.chu_card_val = chu_card
        self.seat_id = seat_id
        return 1

    def clear_other_act(self, **kwargs):  # 清除该玩家其他动作
        timer_manager_ins.kill_timer(self.desk_id, self.seat_id, is_force=True)
        return 1

    def set_data(self, **kwargs):         # 设置相应数据
        ting_info = {}  # TODO 此处调用发放获取具体打什么听什么数据
        # self.players[self.seat_id].hand_card.del_hand_card_by_val(self.chu_card_val)
        self.players[self.seat_id].set_ting_info(self.chu_card_val)
        self.players[self.seat_id].set_can_ting_info({})
        # 记录玩家目前状态
        self.game_data.players[self.seat_id].hand_card.is_ting = 1
        # 是否是天听
        if len(self.game_data.players[self.seat_id].hand_card.drewed_card_lst) == 1 and not self._is_first_has_chi_peng():
            self.game_data.players[self.seat_id].hand_card.is_tian_ting = 1
        return 1

    def record(self, **kwargs):           # 记录玩家动作
        act_record = ActRecord(self.seat_id, Act.TING, self.chu_card_val)
        self.game_data.act_record_list.append(act_record)
        self.players[self.seat_id].hand_card.record_ting_info(self.chu_card_val, self.players[self.seat_id].ting_info)
        return 1

    def notify_other_player(self, **kwargs):  # 记录玩家动作
        # 如果本房间有过户加倍规则, 且玩家听牌, 则可以看到对方玩家所有牌及操作
        game_config = self.game_data.game_config.vars_to_dict()
        special_rule = ujson.loads(game_config.get("special_rule"))
        pass_hu_double = special_rule.get("pass_hu_double")
        all_hand_cards={}
        print("pass_hu_double=", pass_hu_double)
        if pass_hu_double:
            for x in range(self.game_data.max_player_num):
                all_hand_cards[x] = {"hand_card": self.players[x].hand_card.hand_card_vals,
                                     "an_gang_cards": self.players[x].hand_card.get_an_gang_vals}
        act_info = {"seat_id": self.seat_id,
                    "act_type": Act.TING,
                    "card_list": [self.chu_card_val],
                    "all_hand_cards":all_hand_cards}
        self.notify_other_player_act_ting(self.seat_id,
                                          act_info=act_info,
                                          max_player_num=self.game_data.max_player_num)
        return 1

    def clear_lou_hu(self, **kwargs):     # 清除漏胡数据
        return 1

    def after_ting(self, **kwargs):       # 玩家听牌后
        next_seat_id = self.get_next_seat_id(self.seat_id)
        params = {}
        params["seat_id"] = self.seat_id
        params["act_type"] = Act.CHU
        params["act_params"] = {"card": self.chu_card_val}
        CallbackManager.get_instance(self.desk_id).execute(call_func_type=CallbackFuncType.FUNC_PLAYER_ACT,
                                                           call_params=params)
        # self.check_against(self.seat_id, self.chu_card_val)

        # # 通知玩家
        # print "check_ting_chu_against:", self.game_data.cur_players_to_act, self.seat_id, next_seat_id
        # if self.game_data.cur_players_to_act:
        #
        #
        #     cur_act_param = self.game_data.get_player_can_speaker(self.seat_id)
        #
        #     # self.notify_player_to_act(self.seat_id, act_info=cur_act_param, interval=1)
        #     return 1
        # else:
        #     # 没有玩家可以操作时通知下家摸牌
        #     return self.draw_card(next_seat_id)

    def _is_first_has_chi_peng(self):
        if len(self.game_data.act_record_list) != 1:
            return False
        for act in self.game_data.act_record_list:
            if act.act_type in [20, 30]:
                return True
        return False