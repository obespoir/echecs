# coding=utf-8

__author__ = 'jamon'

from obespoir.share.ob_log import logger
from share.message_ids import *
from service.mahjong.models.playeract.base_player_act import BasePlayerAct
from service.mahjong.constants.gamedefine import Act
from service.mahjong.constants.carddefine import BLACK
from service.mahjong.models.actrecord import ActRecord
from service.mahjong.models.card.card import Card
from service.mahjong.controls.notifybridge import notify_single_user
from service.mahjong.models.timermanager import timer_manager_ins


class BuGang(BasePlayerAct):
    def __init__(self, game_data):
        super(BuGang, self).__init__(game_data=game_data)
        self.step_handlers = {
            "param_check": self.param_check,  # 参数验证
            "clear_other_act": self.clear_other_act,  # 清除该玩家其他动作
            "set_data": self.set_data,  # 设置相应数据
            "record": self.record,  # 记录玩家动作
            "notify_other_player": self.notify_other_player,# 记录玩家动作
            "clear_lou_hu": self.clear_lou_hu,  # 清除漏胡数据
            "draw_gang_card": self.draw_gang_card  # 杠后摸牌
        }

        self.seat_id = -1  # 执行出牌的玩家位置
        self.bugang_cardval = BLACK   # 补杠的牌

    def execute(self, act_params={}):
        """
        执行补杠
        :param act_params:
        :return:
        """
        logger.debug(u"补杠: %s", str(act_params))
        for step in self.game_config.player_act_step.get(Act.BU_GANG):
            for name, cfg in step.items():
                ret = self.step_handlers.get(name)(act_params=act_params, config_params=cfg)
                if not ret:
                    logger.error("step:%s", step)
                    return
        return 1

    def param_check(self, **kwargs):      # 参数验证
        act_params = kwargs.get("act_params")
        # if 1 != len(act_params):
        #     # 同时只允许有一个玩家发生补杠牌操作
        #     logger.debug(u"act_bugang_error:%s", str(act_params))
        #     return

        seat_id = list(act_params.keys())[0]
        params = act_params[seat_id]
        # TODO 此处需要接受参数 用户选择暗杠牌值
        used_card = params.get("used_card")[0]

        if not used_card:
            logger.error("bu_gang card_val is none error: %s", str([self.seat_id, params]))
            return

        hand_card = self.players[seat_id].hand_card
        if 1 != used_card and [used_card, used_card, used_card] not in hand_card.peng_card_vals:
            logger.error("bu_gang card_val not in peng_card_val error: %s", str([self.seat_id, params]))
            return

        self.bugang_cardval = used_card
        self.seat_id = seat_id
        return 1

    def clear_other_act(self, **kwargs):  # 清除该玩家其他动作
        timer_manager_ins.kill_timer(self.desk_id, self.seat_id, is_force=True)
        return 1

    def set_data(self, **kwargs):         # 设置相应数据
        self.players[self.seat_id].hand_card.del_hand_card_by_val_list([self.bugang_cardval])

        # 全局可见的牌中添加吃牌
        self.game_data.add_chu_card(self.bugang_cardval)
        return 1

    def record(self, **kwargs):           # 记录玩家动作
        cards = [self.bugang_cardval]
        act_record = ActRecord(self.seat_id, Act.BU_GANG, cards)
        self.game_data.act_record_list.append(act_record)
        self.players[self.seat_id].hand_card.record_bu_gang_card(self.bugang_cardval)
        return 1

    def notify_other_player(self, **kwargs):  # 记录玩家动作
        act_info = {"seat_id": self.seat_id, "act_type": Act.BU_GANG, "card_list": [self.bugang_cardval]}
        self.notify_other_player_act_executed(self.seat_id,
                                              act_info=act_info,
                                              max_player_num=self.game_data.max_player_num)
        return 1

    def clear_lou_hu(self, **kwargs):     # 清除漏胡数据
        return 1

    def draw_gang_card(self, **kwargs):   # 杠后摸牌
        self.draw_card(self.seat_id, is_last=True)
        return 1

