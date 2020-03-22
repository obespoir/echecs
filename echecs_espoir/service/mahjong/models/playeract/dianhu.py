# coding=utf-8

__author__ = 'jamon'
import copy

from obespoir.share.ob_log import logger
from share.message_ids import *
from service.mahjong.models.playeract.base_player_act import BasePlayerAct
from service.mahjong.constants.gamedefine import Act, SettleType
from service.mahjong.models.actrecord import ActRecord
from service.mahjong.models.timermanager import timer_manager_ins


class DianHu(BasePlayerAct):
    def __init__(self, game_data):
        super(DianHu, self).__init__(game_data=game_data)
        self.step_handlers = {
            "param_check": self.param_check,            # 参数验证
            "clear_other_act": self.clear_other_act,    # 清除该玩家其他动作
            "set_data": self.set_data,                  # 设置相应数据
            "record": self.record,                      # 记录玩家动作
            "notify_other_player": self.notify_other_player,  # 记录玩家动作
        }

        self.seat_id = -1       # 执行胡牌的玩家位置
        self.hook_seat_id = -1  # 是否为抢胡, 如抢补杠胡
        self.hand_card = None
        self.dian_hu_card = 0   # 点炮的那张牌

    def execute(self, act_params={}):
        """
        执行点炮胡牌
        :param act_params:
        :return:
        """
        logger.debug(u"点炮胡牌: %s", str(act_params))
        for seat_id, params in act_params.items():
            for step in self.game_config.player_act_step.get(Act.DIAN_HU):
                for name, cfg in step.items():
                    ret = self.step_handlers.get(name)(seat_id=seat_id, params=params, config_params=cfg)
                    if not ret:
                        logger.error("step:%s", step)
                        return
            if not self.game_config.has_tong_pao:
                # 如果不能通炮胡，则只取第一个胡牌的玩家
                break
        self.settle(settle_type_list=[SettleType.HU])
        if self.game_config.is_hu_end:
            # 当回合胡牌后结束当局游戏
            self.end_game()
        return 1

    def param_check(self, seat_id, params, config_params):      # 参数验证
        hook_seat_id = params.get("hook_seat_id", -1)

        if not self.game_data.last_chu_card_val:
            logger.error("dian_hu params error: %s", str([seat_id, params]))
            return

        hand_card_vals = self.players[seat_id].hand_card.hand_card_vals
        # if 1 != len(hand_card_vals) % 3 or not self.players[seat_id].can_hu_result:
        if 1 != len(hand_card_vals) % 3:
            logger.error("dian_hu params error: %s", str([seat_id, params]))
            return

        self.seat_id = seat_id
        self.hook_seat_id = hook_seat_id
        self.hand_card = self.game_data.players[seat_id].hand_card
        self.dian_hu_card = self.game_data.last_chu_card_val
        return 1

    def clear_other_act(self, seat_id, params, config_params):  # 清除该玩家其他动作
        timer_manager_ins.kill_timer(self.desk_id, self.seat_id, is_force=True)
        return 1

    def set_data(self, seat_id, params, config_params):         # 设置相应数据
        self.players[self.seat_id].hook_hu_seat_id = self.hook_seat_id    # 抢胡来源座位id
        self.players[self.seat_id].hand_card.qiang_gang_hu_seat_id = self.hook_seat_id    # 抢胡来源座位id
        # 将手牌信息保存入 hand_card_for_settle_show
        self.game_data.players[self.seat_id].hand_card.hand_card_for_settle_show[-1] = [self.game_data.last_chu_card_val]
        # 储存胡的牌值
        self.game_data.players[self.seat_id].hand_card.hu_card_val = self.game_data.last_chu_card_val

        # 吃碰杠时,移除提供吃碰杠玩家已出牌里面的 那一张
        self.players[self.game_data.last_chu_card_seat_id].hand_card.out_card_vals.remove(
            self.game_data.last_chu_card_val)
        # 联合手牌
        for i in range(self.game_data.max_player_num):
            self.game_data.players[i].hand_card.union_hand_card()
        # 计算结算相关数据,用于101006
        type_list = self.game_data.hu_manager.check_hu_result(self.hand_card, self.dian_hu_card)
        self.game_data.hu_player_static[self.seat_id] = {
            "type_list": type_list,
            "is_zi_mo": 0,
            "source_seat_id": self.game_data.last_chu_card_seat_id,
            "guo_hu_count": self.game_data.players[self.seat_id].hand_card.guo_hu_num,
            "settle_hand_card": self.game_data.players[self.seat_id].hand_card.hand_card_for_settle_show
        }
        # 判断是否是点胡
        if self._is_first_chu_card():
            self.players[self.seat_id].hand_card.is_ren_hu = 1
        return 1

    def record(self, seat_id, params, config_params):           # 记录玩家动作
        act_record = ActRecord(self.seat_id, Act.DIAN_HU, [self.game_data.last_chu_card_val])
        self.game_data.act_record_list.append(act_record)
        self.players[self.seat_id].hand_card.record_dian_hu_card(self.game_data.last_chu_card_seat_id,
                                                            self.game_data.last_chu_card_val)
        return 1

    def notify_other_player(self, **kwargs):  # 通知其他玩家动作已经执行
        act_info = {"seat_id": self.seat_id,
                    "act_type": Act.DIAN_HU,
                    "card_list": self.dian_hu_card}
        self.notify_other_player_act_executed(self.seat_id,
                                              act_info=act_info,
                                              max_player_num=self.game_data.max_player_num)
        return 1


    def _is_first_chu_card(self):
        if len(self.game_data.act_record_list) >1 :
            return False
        if self.game_data.act_record_list[0].act_type == 10:
            return True
        return False
