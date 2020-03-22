# coding=utf-8

__author__ = 'jamon'

from obespoir.share.ob_log import logger
from service.mahjong.models.playeract.base_player_act import BasePlayerAct
from service.mahjong.constants.gamedefine import Act
from service.mahjong.models.actrecord import ActRecord
from service.mahjong.models.timermanager import timer_manager_ins


class Chi(BasePlayerAct):
    def __init__(self, game_data):
        super(Chi, self).__init__(game_data=game_data)
        self.step_handlers = {
            "param_check": self.param_check,                # 参数验证
            "clear_other_act": self.clear_other_act,        # 清除该玩家其他动作
            "set_data": self.set_data,                      # 设置相应数据
            "record": self.record,                          # 记录玩家动作
            "notify_other_player": self.notify_other_player,# 记录玩家动作
            "clear_lou_hu": self.clear_lou_hu,              # 清除漏胡数据
            "after_chi": self.after_chi                     # 吃动作之后，通知玩家叫牌
        }

        self.used_cards = []       # 吃牌使用的牌
        self.chi_group = []        # 吃牌的组合
        self.seat_id = -1          # 执行出牌的玩家位置

    def reset_data(self):
        self.used_cards = []  # 吃牌使用的牌
        self.chi_group = []   # 吃牌的组合
        self.seat_id = -1     # 执行出牌的玩家位置

    def execute(self, act_params={}):
        """
        执行吃牌
        :param act_params:
        :return:
        """
        logger.debug(u"吃牌: %s", str(act_params))
        print("CHI EXECUTE self.game_config.player_act_step=", self.game_config.player_act_step)
        print("CHI_step=", self.game_config.player_act_step.get(Act.CHI))
        for step in self.game_config.player_act_step.get(Act.CHI):
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
            logger.debug(u"act_chi_error:%s", str(act_params))
            return

        seat_id = list(act_params.keys())[0]
        params = act_params[seat_id]

        card_val = self.game_data.last_chu_card_val
        used_cards = params.get("used_card", [])
        # 接受三张牌,用户吃的牌, 出去被吃的牌做处理
        if card_val not in used_cards:
            logger.error("chi card val not in used_cards params error: %s", str([seat_id, params]))
            return
        used_cards.remove(card_val)
        if not card_val or 2 != len(used_cards):
            logger.error("chi params error: %s", str([seat_id, params]))
            return

        hand_card_vals = self.players[seat_id].hand_card.hand_card_vals
        if used_cards[0] not in hand_card_vals or used_cards[1] not in hand_card_vals:
            logger.error("chi params error: %s", str([seat_id, params]))
            return

        cards = [card_val, used_cards[0], used_cards[1]]
        cards.sort()
        if not self.card_analyse.shun(cards):
            logger.error("chi params error: %s", str([seat_id, params]))
            return

        self.used_cards = used_cards
        self.chi_group = cards
        self.seat_id = seat_id
        return 1

    def clear_other_act(self, **kwargs):  # 清除该玩家其他动作
        timer_manager_ins.kill_timer(self.desk_id, self.seat_id, is_force=True)
        return 1

    def set_data(self, **kwargs):         # 设置相应数据
        self.players[self.seat_id].hand_card.del_hand_card_by_val_list(self.used_cards)
        # 吃碰杠时,移除提供吃碰杠玩家已出牌里面的 那一张
        self.players[self.game_data.last_chu_card_seat_id].hand_card.out_card_vals.remove(self.game_data.last_chu_card_val)
        self.game_data.add_player_to_act(self.seat_id, Act.CHU, act_params={"card": self.used_cards})
        # 全局可见的牌中添加吃牌
        self.game_data.add_chu_card(self.used_cards)

        return 1

    def record(self, **kwargs):           # 记录玩家动作
        act_record = ActRecord(self.seat_id, Act.CHI, self.chi_group)
        self.game_data.act_record_list.append(act_record)
        self.players[self.seat_id].hand_card.record_chi_card(self.game_data.last_chu_card_val, self.used_cards)
        return 1

    def notify_other_player(self, **kwargs):  # 记录玩家动作
        act_info = {"seat_id": self.seat_id,
                    "act_type": Act.CHI,
                    "card_list": self.chi_group,
                    "hand_card": self.players[self.seat_id].hand_card.hand_card_vals}
        self.notify_other_player_act_executed(self.seat_id,
                                              act_info=act_info,
                                              max_player_num=self.game_data.max_player_num)
        return 1


    def clear_lou_hu(self, **kwargs):     # 清除漏胡数据
        return 1

    def after_chi(self, **kwargs):       # 吃动作之后，通知玩家叫牌
        cfg = kwargs.get("config_params")
        can_ting = cfg.get("can_ting", 0)
        if can_ting:
            ting_results = self.game_data.hu_manager.check_ting_result(self.players[self.seat_id].hand_card)
            if ting_results:
                self.notify_player_ting(self.seat_id, ting_results)
            else:
                chu_card = self.players[self.seat_id].hand_card.hand_card_vals[-1]
                self.notify_player_to_act(self.seat_id, act_info={Act.CHU: {"card": chu_card}},
                                          interval=self.get_act_wait_time(self.seat_id))
        else:
            chu_card = self.players[self.seat_id].hand_card.hand_card_vals[-1]
            self.notify_player_to_act(self.seat_id, act_info={Act.CHU: {"card": chu_card}},
                                      interval=self.get_act_wait_time(self.seat_id))
        return 1


