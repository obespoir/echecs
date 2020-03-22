# coding=utf-8

__author__ = 'jamon'

from obespoir.share.ob_log import logger
from share.message_ids import *
from service.mahjong.models.playeract.base_player_act import BasePlayerAct
from service.mahjong.constants.gamedefine import Act
from service.mahjong.models.actrecord import ActRecord
from service.mahjong.models.card.card import Card
from service.mahjong.models.timermanager import timer_manager_ins


class DianGang(BasePlayerAct):
    def __init__(self, game_data):
        super(DianGang, self).__init__(game_data=game_data)
        self.step_handlers = {
            "param_check": self.param_check,          # 参数验证
            "clear_other_act": self.clear_other_act,  # 清除该玩家其他动作
            "set_data": self.set_data,                # 设置相应数据
            "record": self.record,                    # 记录玩家动作
            "notify_other_player": self.notify_other_player,  # 记录玩家动作
            "clear_lou_hu": self.clear_lou_hu,        # 清除漏胡数据
            "draw_gang_card": self.draw_gang_card     # 杠后摸牌
        }

        self.seat_id = -1  # 执行出牌的玩家位置
        self.hand_card = None

    def execute(self, act_params={}):
        """
        执行点杠
        :param act_params:
        :return:
        """
        logger.debug(u"点杠: %s", str(act_params))
        for step in self.game_config.player_act_step.get(Act.DIAN_GANG):
            for name, cfg in step.items():
                ret = self.step_handlers.get(name)(act_params=act_params, config_params=cfg)
                if not ret:
                    logger.error("step:%s", step)
                    return
        return 1

    def param_check(self, **kwargs):      # 参数验证
        act_params = kwargs.get("act_params")
        if 1 != len(act_params):
            # 同时只允许有一个玩家发生点杠操作
            logger.debug(u"act_diangang_error:%s", str(act_params))
            return

        seat_id = list(act_params.keys())[0]
        params = act_params[seat_id]

        card_val = self.game_data.last_chu_card_val

        if not card_val or -1 == self.game_data.last_chu_card_seat_id:
            logger.error("dian_gang params error: %s", str([seat_id, params]))
            return

        hand_card = self.players[seat_id].hand_card
        if 3 != hand_card.hand_card_info[Card.cal_card_type(card_val)][Card.cal_card_digit(card_val)]:
            logger.error("dian_gang params error: %s", str([seat_id, params]))
            return

        self.seat_id = seat_id
        self.hand_card = self.game_data.players[seat_id].hand_card
        return 1

    def clear_other_act(self, **kwargs):  # 清除该玩家其他动作
        timer_manager_ins.kill_timer(self.desk_id, self.seat_id, is_force=True)
        return 1

    def set_data(self, **kwargs):         # 设置相应数据

        card_val = self.game_data.last_chu_card_val
        self.players[self.seat_id].hand_card.del_hand_card_by_val_list([card_val, card_val, card_val])
        # 吃碰杠时,移除提供吃碰杠玩家已出牌里面的 那一张
        self.players[self.game_data.last_chu_card_seat_id].hand_card.out_card_vals.remove(
            self.game_data.last_chu_card_val)
        # 全局可见的牌中添加吃牌
        self.game_data.add_chu_card([self.game_data.last_chu_card_val for _ in range(3)])
        return 1

    def record(self, **kwargs):           # 记录玩家动作
        card_val = self.game_data.last_chu_card_val
        cards = [card_val]
        act_record = ActRecord(self.seat_id, Act.DIAN_GANG, cards)
        self.game_data.act_record_list.append(act_record)
        self.players[self.seat_id].hand_card.record_dian_gang_card(self.game_data.last_chu_card_seat_id, card_val)
        return 1

    def notify_other_player(self, **kwargs):  # 记录玩家动作
        act_info = {"seat_id": self.seat_id, "act_type": Act.DIAN_GANG, "card_list": [self.game_data.last_chu_card_val]}
        self.notify_other_player_act_executed(self.seat_id,
                                              act_info=act_info,
                                              max_player_num=self.game_data.max_player_num)
        return 1

    def clear_lou_hu(self, **kwargs):     # 清除漏胡数据
        return 1

    def draw_gang_card(self, **kwargs):   # 杠后摸牌
        self.draw_card(self.seat_id, is_last=True)
        return 1
