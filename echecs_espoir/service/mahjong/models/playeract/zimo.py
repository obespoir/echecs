# coding=utf-8

__author__ = 'jamon'
import copy
from obespoir.share.ob_log import logger
from share.message_ids import *
from service.mahjong.models.playeract.base_player_act import BasePlayerAct
from service.mahjong.constants.gamedefine import Act, SettleType
from service.mahjong.models.actrecord import ActRecord
from service.mahjong.models.timermanager import timer_manager_ins
from service.mahjong.controls.notifybridge import notify_single_user


class ZiMo(BasePlayerAct):
    def __init__(self, game_data):
        super(ZiMo, self).__init__(game_data=game_data)
        self.step_handlers = {
            "param_check": self.param_check,  # 参数验证
            "clear_other_act": self.clear_other_act,  # 清除该玩家其他动作
            "set_data": self.set_data,  # 设置相应数据
            "record": self.record,  # 记录玩家动作
            "notify_other_player": self.notify_other_player,  # 通知其他玩家
        }

        self.seat_id = -1  # 执行胡牌的玩家位置
        self.type_list = []  # 胡牌的胡牌类型
        self.hand_card = None

    def execute(self, act_params={}):
        """
        执行自摸
        :param act_params:
        :return:
        """
        logger.debug(u"自摸胡牌: %s", str(act_params))
        for step in self.game_config.player_act_step.get(Act.ZI_MO):
            for name, cfg in step.items():
                ret = self.step_handlers.get(name)(act_params=act_params, config_params=cfg)
                if not ret:
                    logger.error("step:%s", step)
                    return

        self.settle(settle_type_list=[SettleType.HU])
        if self.game_config.is_hu_end:
            # 当回合胡牌后结束当局游戏
            self.end_game()
        return 1

    def param_check(self, **kwargs):      # 参数验证
        act_params = kwargs.get("act_params")
        if 1 != len(act_params):
            # 同时只允许有一个玩家发生自摸操作
            logger.debug(u"act_zimo_error:%s", str(act_params))
            return

        seat_id = list(act_params.keys())[0]
        params = act_params[seat_id]

        hand_card_vals = self.players[seat_id].hand_card.hand_card_vals
        # if 2 != len(hand_card_vals) % 3 or not self.players[seat_id].can_hu_result:
        if 2 != len(hand_card_vals) % 3:
            logger.error("dian_hu params error: %s", str([seat_id, params]))
            return

        self.seat_id = seat_id
        self.hand_card = self.players[seat_id].hand_card
        return 1

    def clear_other_act(self, **kwargs):  # 清除该玩家其他动作
        timer_manager_ins.kill_timer(self.desk_id, self.seat_id, is_force=True)
        return 1

    def set_data(self, **kwargs):         # 设置相应数据
        # 记录自摸信息
        self.game_data.players[self.seat_id].hand_card.zi_mo = 1
        # 将手牌信息保存入 hand_card_for_settle_show 用于游戏结束手牌的展示
        # self.game_data.players[self.seat_id].hand_card.hand_card_for_settle_show[-1] = [self.game_data.last_get_card_val[self.seat_id]]
        # 储存胡的牌值
        self.game_data.players[self.seat_id].hand_card.hu_card_val = self.game_data.last_get_card_val[self.seat_id]
        # 联合手牌,用于计算胡牌番型
        for i in range(self.game_data.max_player_num):
            self.game_data.players[i].hand_card.union_hand_card()

        # 计算结算相关数据,用于101006
        type_list = self.game_data.hu_manager.check_hu_result(self.hand_card)
        self.game_data.hu_player_static[self.seat_id] = {
            "type_list": type_list,
            "is_zi_mo": 1,
            "source_seat_id": -1,
            "guo_hu_count": self.game_data.players[self.seat_id].hand_card.guo_hu_num,
            "settle_hand_card": self.game_data.players[self.seat_id].hand_card.hand_card_for_settle_show
        }
        # 是否天地胡牌
        if len(self.players[self.seat_id].hand_card.drewed_card_lst) == 1 and self._is_first_has_chi_peng():
            if self.seat_id == self.game_data.banker_seat_id:
                # 天胡
                self.players[self.seat_id].hand_card.is_tian_hu = 1
            else:
                # 地胡
                self.players[self.seat_id].hand_card.is_di_hu = 1

        return 1

    def record(self, **kwargs):           # 记录玩家动作
        act_record = ActRecord(self.seat_id, Act.ZI_MO, [])
        self.game_data.act_record_list.append(act_record)
        return 1


    def notify_other_player(self, **kwargs):  # 记录玩家动作
        act_info = {"seat_id": self.seat_id, "act_type": Act.ZI_MO, "card_list": []}
        for i in range(self.game_data.max_player_num):
            notify_single_user(self.desk_id, self.seat_id, PUSH_OTHER_PLAYER_CALL_CARD, act_info)
        return 1

    def _is_first_has_chi_peng(self):
        if len(self.game_data.act_record_list) != 1:
            return False
        for act in self.game_data.act_record_list:
            if act.act_type in [20, 30]:
                return True
        return False