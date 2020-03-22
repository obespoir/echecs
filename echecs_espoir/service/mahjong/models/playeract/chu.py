# coding=utf-8

__author__ = 'jamon'

from obespoir.share.ob_log import logger
from share.message_ids import *
from service.mahjong.models.playeract.base_player_act import BasePlayerAct
from service.mahjong.constants.gamedefine import Act, SystemActType, GameActStatus
from service.mahjong.constants.carddefine import BLACK
from service.mahjong.models.actrecord import ActRecord
from service.mahjong.models.card.card import Card
from service.mahjong.controls.notifybridge import notify_single_user
from service.mahjong.models.timermanager import timer_manager_ins
from service.mahjong.models.callbackmanager import CallbackFuncType


class Chu(BasePlayerAct):
    def __init__(self, game_data):
        super(Chu, self).__init__(game_data=game_data)
        self.step_handlers = {
            "param_check": self.param_check,                  # 参数验证
            "clear_other_act": self.clear_other_act,          # 清除该玩家其他动作
            "set_data": self.set_data,                        # 设置相应数据
            "record": self.record,                            # 记录玩家动作
            "notify_other_player": self.notify_other_player,  # 通知其他玩家
            "check_chu_against": self.check_chu_against       # 检查其他玩家可进行的操作
        }

        self.seat_id = -1  # 执行出牌的玩家位置
        self.chu_cardval = BLACK

    def execute(self, act_params={}):
        """
        执行出牌
        :param act_params:
        :return:
        """
        logger.debug(u"出牌: %s", str(act_params))

        for step in self.game_config.player_act_step.get(Act.CHU):
            for name, cfg in step.items():
                ret = self.step_handlers.get(name)(act_params=act_params, config_params=cfg)
                if not ret:
                    logger.error("step:%s", step)
                    return
        return 1

    def param_check(self, **kwargs):      # 参数验证
        act_params = kwargs.get("act_params")
        if 1 != len(act_params):
            # 同时只允许有一个玩家发生出牌操作
            logger.debug(u"act_chu_error:%s", str(act_params))
            return

        seat_id = list(act_params.keys())[0]
        params = act_params[seat_id]

        card_val = params.get("card", None)
        if isinstance(card_val, list):
            card_val = card_val[0]
        if not card_val:
            logger.debug(u"chu_card error: card_val=%s", str(card_val))
            return
        if 1 > self.players[seat_id].hand_card.hand_card_info[Card.cal_card_type(card_val)][Card.cal_card_digit(card_val)]:
            logger.debug(u"chu_card error: not hava card %s", str([seat_id, params]))
            return

        self.seat_id = seat_id
        self.chu_cardval = card_val
        return 1

    def clear_other_act(self, **kwargs):  # 清除该玩家其他动作
        timer_manager_ins.kill_timer(self.desk_id, self.seat_id, is_force=True)
        return 1

    def set_data(self, **kwargs):         # 设置相应数据
        self.game_data.add_chu_card(self.chu_cardval)
        cur_player = self.players[self.seat_id]
        cur_player.chu_card(self.chu_cardval)
        self.game_data.last_chu_card_val = self.chu_cardval
        # self.game_data.clear_cur_speaker(self.seat_id)
        # 当出牌时候,更新最后出牌人的作为ID
        self.game_data.last_chu_card_seat_id = self.seat_id
        # 当前牌局上正在操作的那张牌
        self.game_data.cur_deal_card_val = self.chu_cardval
        return 1

    def record(self, **kwargs):           # 记录玩家动作
        act_record = ActRecord(self.seat_id, Act.CHU, [self.chu_cardval])
        self.game_data.act_record_list.append(act_record)
        return 1

    def notify_other_player(self, **kwargs):           # 记录玩家动作
        act_info = {"seat_id": self.seat_id, "act_type": Act.CHU, "card_list": [self.chu_cardval]}
        self.notify_other_player_act_executed(self.seat_id,
                                              act_info=act_info,
                                              max_player_num=self.game_data.max_player_num)
        logger.debug(u"seat_id=%s, hand_card=%s len=%s" %(self.seat_id,
                                                 self.players[self.seat_id].hand_card.hand_card_vals,
                                                 len(self.players[self.seat_id].hand_card.hand_card_vals)))
        return 1

    def check_chu_against(self, **kwargs):     # 检查出牌后是否有玩家可操作
        next_seat_id = self.get_next_seat_id(self.seat_id)
        self.check_against(self.seat_id, self.chu_cardval)

        # 通知玩家
        print("check_chu_against:", self.game_data.cur_players_to_act, self.seat_id, next_seat_id)
        if self.game_data.cur_players_to_act:
            for i in range(self.max_player_num):
                act_list = self.game_data.get_player_can_speaker(i)
                if act_list:
                    # data = {
                    #     "command_id": PUSH_CALL_CARD, "seat_id": i,
                    #     "act": act_list, "card": self.chu_cardval, "is_against": 1
                    # }
                    # notify_single_user(self.desk_id, self.seat_id, PUSH_CALL_CARD, data)
                    self.notify_player_to_act(i, act_info=act_list, interval=self.get_act_wait_time(i))
            self.game_data.next_speaker_callback = {"type": CallbackFuncType.FUNC_DRAW_CARD,
                                                    "call_params": {"seat_id": next_seat_id}}
            return 1
        else:
            # 没有玩家可以操作时通知下家摸牌
            return self.draw_card(next_seat_id)
