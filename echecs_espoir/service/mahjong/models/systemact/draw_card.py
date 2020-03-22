# coding=utf-8


from service.mahjong.models.systemact.base_system_act import BaseSystemAct
from service.mahjong.constants.carddefine import CardType, CARD_SIZE, BLACK
from service.mahjong.constants.gamedefine import Act, CheckSelfActType, CheckNameTypeRel, SystemActType, TimerType, SettleType
from service.mahjong.controls.notifybridge import notify_single_user, notify_all_desk_player
from service.mahjong.models.card.card import Card
from service.mahjong.constants.carddefine import LAI_ZI
from service.mahjong.models.systemact.system_act_manager import SystemActManager
from service.mahjong.models.timermanager import timer_manager_ins
from service.mahjong.models.callbackmanager import CallbackFuncType
from config.globalconfig import GlobalConfig
from obespoir.share.ob_log import logger
from share.message_ids import *


class DrawCard(BaseSystemAct):
    """摸牌"""

    def __init__(self, game_data):
        super(DrawCard, self).__init__(game_data=game_data)
        self.step_handlers = {
            "param_check": self.param_check,            # 参数验证
            "has_enough_card": self.has_enough_card,    # 是否有足够的牌
            "set_data": self.set_data,                  # 设置相应数据
            "notify_drew_card": self.notify_drew_card,  # 通知已摸到的牌
            "check_after": self.check_after             # 摸牌后检查玩家可进行的操作
        }

        self.check_handler = {
            CheckSelfActType.CAN_AN_GANG: self.can_an_gang,
            CheckSelfActType.CAN_BU_GANG: self.can_bu_gang,
            CheckSelfActType.CAN_ZI_MO: self.can_zi_mo,
            CheckSelfActType.CAN_TING: self.can_ting
        }

        self.seat_id = -1         # 当前摸牌玩家的座位号
        self.card_num = 0         # 当次摸牌的张数
        self.is_last = False      # 当次摸牌从牌头还是牌尾
        self.drew_cardvals = []   # 存放摸到的牌

    def execute(self, seat_id, card_num=1, is_last=False):
        """
        执行摸牌
        :param seat_id:
        :param card_num:
        :param is_last:
        :return:
        """
        logger.debug(u"摸牌: %s", str([seat_id, card_num, is_last]))
        print("### sid=%s draw_card len=%s hand-card =%s ," % (seat_id,
            len(self.players[seat_id].hand_card.hand_card_vals), self.players[seat_id].hand_card.hand_card_vals))
        for step in self.game_config.draw_card_step:
            for name, cfg in step.items():
                ret = self.step_handlers.get(name)(seat_id=seat_id, card_num=card_num, is_last=is_last, config_params=cfg)
                if not ret:
                    logger.error("step:%s", step)
                    return
                elif ret != 1:
                    return 0
        return 1

    def param_check(self, **kwargs):
        """参数验证"""
        seat_id = kwargs.get("seat_id", -1)
        card_num = kwargs.get("card_num", 0)
        is_last = kwargs.get("is_last", False)
        if 0 > seat_id or 0 >= card_num:
            logger.debug(u"param_check error:%s", str(kwargs))
            return 0
        self.seat_id = seat_id
        self.card_num = card_num
        self.is_last = is_last
        return 1

    def has_enough_card(self, **kwargs):
        """
        判断牌堆中是否还有足够的牌, 返回-1表示牌数不够，不进行下一步操作
        """
        if self.card_dealer.card_count < self.card_num + self.game_data.get_min_left_cards():
            logger.debug(u"摸牌牌数不够: %s", str([self.seat_id, self.card_num, self.is_last]))
            # 遊戲结算
            SystemActManager.get_instance(self.desk_id).system_act(
                act_type=SystemActType.SETTLE, act_params={"type_list": [SettleType.DRAW]})
            # 遊戲結束
            SystemActManager.get_instance(self.desk_id).system_act(
                act_type=SystemActType.GAME_OVER, act_params={})
            return -1
        return 1

    def set_data(self, **kwargs):
        self.drew_cardvals = []
        for i in range(self.card_num):
            if self.game_data.max_player_num == 2:
                self.drew_cardvals.append(self.card_dealer.draw_a_card_first_without_hua(
                    is_last=self.is_last,
                    seat_id=self.seat_id,
                    card_list=GlobalConfig().test_sure_next_cards.get(self.desk_id,[[],[],[],[]])))
            else:
                self.drew_cardvals.append(self.card_dealer.draw_a_card(is_last=self.is_last))

        self.players[self.seat_id].hand_card.add_hand_card_by_vals(self.drew_cardvals)
        # 将最近入手的牌装入game_data
        self.game_data.last_get_card_val[self.seat_id] = self.drew_cardvals[0]
        # 当前牌局上正在操作的那张牌
        self.game_data.cur_deal_card_val = self.drew_cardvals[0]
        return 1

    def notify_drew_card(self, **kwargs):
        """通知桌子上所有玩家该玩家已摸牌"""
        for x in self.players:
            if x.seat_id == self.seat_id or self.game_data.players[x.seat_id].hand_card.is_ting:
                data = {"seat_id": self.seat_id,
                        "card_list": self.drew_cardvals,
                        "remain_count": self.game_data.card_dealer.get_remain_count}
            else:
                # 当处于过胡加倍场, 且当前用户上听了, 则开始上帝模式
                if x.hand_card.is_ting and self.game_config.pass_hu_double:
                    card_list = self.drew_cardvals
                else:
                    card_list = [BLACK] * self.card_num
                data = {"seat_id": self.seat_id,
                        "card_list": card_list,
                        "remain_count": self.game_data.card_dealer.get_remain_count}

            notify_single_user(self.desk_id, x.seat_id, PUSH_DRAW_CARD, data=data)
        return 1

    def check_after(self, **kwargs):
        """
        摸牌后检查玩家可进行的操作
        :return: []
        """
        if self.game_config.draw_card_bu_hua and self.bu_hua():
            # 如果有补花存在,则不进行下一步的检查操作
            return 1

        hand_card = self.players[self.seat_id].hand_card
        can_op_info = {}

        for check in self.game_config.draw_card_check_list:
            ret = self.check_handler.get(check)(hand_card)
            if ret:
                act_type = CheckNameTypeRel.REL.get(check)
                can_op_info[act_type] = ret
                self.game_data.add_player_to_act(self.seat_id, act_type, act_params=ret)

        if self.game_data.state_machine.players[self.seat_id].hand_card.is_ting:
            chu_card = self.game_data.last_get_card_val[self.seat_id]
        else:
            chu_card = self.players[self.seat_id].hand_card.hand_card_vals[-1]
        if self.game_data.cur_players_to_act.get(self.seat_id, {}):
            self.game_data.add_player_to_act(self.seat_id, Act.GUO, act_params={})
            # 根据不同动作获取不同操作时间
            can_op_act = Act.GUO
            if can_op_info.keys():
                can_op_act = list(can_op_info.keys())[0]
            # 非WAITE_ANSWER 情况加添加过动作
            if not self.game_data.cur_players_to_act.get(self.seat_id).get(100):
                can_op_info[Act.GUO] = {}
            self.notify_player_to_act(self.seat_id, act_info=can_op_info,
                                      interval=self.get_act_wait_time(self.seat_id, act_type=can_op_act))
            self.game_data.next_speaker_callback = {"type": CallbackFuncType.FUNC_NOTIFY_PLAYER_ACT, "call_params": {
                "seat_id": self.seat_id, "interval": self.get_act_wait_time(self.seat_id, Act.CHU),
                "act_info": {Act.CHU: {"card": chu_card}}}}
        else:
            # 当前玩家没有任何操作

            self.notify_player_to_act(self.seat_id, act_info={Act.CHU: {"card": chu_card}},
                                      interval=self.get_act_wait_time(self.seat_id))
            self.game_data.del_player_to_act(self.seat_id)
            self.game_data.add_player_to_act(self.seat_id, Act.CHU, act_params={"card": chu_card})
        # 记录各位置玩家所摸过的牌
        for i in self.drew_cardvals:
            self.game_data.players[self.seat_id].hand_card.drewed_card_lst.append(i)
        return 1

    def bu_hua(self):
        """检查是否补花"""
        hua_card = []
        for c in self.drew_cardvals:
            if CardType.HUA == Card.cal_card_type(c):
                hua_card.append(c)
        if not hua_card:
            return 0
        logger.debug('补花：%d', len(hua_card))
        # 将花牌从手牌中移除
        self.players[self.seat_id].hand_card.del_hand_card_by_val(hua_card[0])
        # 将补花数量添加进手牌中
        self.players[self.seat_id].hand_card.hua_card_vals.extend(hua_card)
        # 通知所有人有玩家补花
        notify_all_desk_player(self.desk_id, PUSH_GAME_BU_HUA, {"seat_id": self.seat_id, "hua_card_list": hua_card})
        timer_manager_ins.add_timer(self.desk_id, self.seat_id, GlobalConfig().bu_hua_show_time,
                                    t_type=TimerType.KEEP,
                                    call_type=CallbackFuncType.FUNC_DRAW_CARD,
                                    call_params={"seat_id": self.seat_id, "card_num": len(hua_card), "is_last": True})
        return 1

    def can_an_gang(self, hand_card):
        """是否可以暗杠"""
        if self.players[self.seat_id].ting_info:
            # 玩家处于听牌状态
            return []
        all_types = CardType.all_type()
        can_an_gang_cards = []
        for t in all_types:
            if 4 > hand_card.hand_card_info[t][0]:
                continue
            for i in range(1, CARD_SIZE[t]):
                if 4 == hand_card.hand_card_info[t][i]:
                    can_an_gang_cards.append(Card.cal_card_val(t, i))

        return can_an_gang_cards

    def can_bu_gang(self, hand_card):
        """是否可以补杠"""
        all_types = CardType.all_type()
        can_bu_gang_cards = []
        for t in all_types:
            if 1 > hand_card.hand_card_info[t][0]:
                continue
            for i in range(1, CARD_SIZE[t]):
                if 1 == hand_card.hand_card_info[t][i]:
                    card_val = Card.cal_card_val(t, i)
                    for peng_group in hand_card.peng_card_vals:
                        if card_val in peng_group:
                            if self.players[self.seat_id].ting_info:
                                # 玩家处于听牌状态, 判断补杠后会否破坏牌型
                                temp_cards = self.players[self.seat_id].hand_card.hand_card_vals
                                temp_cards.remove(card_val)
                                temp_cards.append(LAI_ZI)
                                ting_cards = self.card_analyse.get_can_ting_info_by_val(temp_cards)
                                ret = []
                                for k in ting_cards.keys():
                                    ret.extend(ting_cards[k])
                                if not set(self.players[self.seat_id].ting_info.keys()).issubset(set(ret)):
                                    # 如果新的听牌结果不包含原有听牌结果，则不能点杠
                                    print("seat=%s, card_val=%s, ting_cards=%s , can't ting!" % (
                                    self.seat_id, card_val, ting_cards))
                                else:
                                    can_bu_gang_cards.append(card_val)
                            else:
                                can_bu_gang_cards.append(card_val)

        return can_bu_gang_cards

    def can_zi_mo(self, hand_card):
        """是否可自摸"""
        type_list = self.game_data.hu_manager.check_hu_result(hand_card)
        ret = {}
        if type_list:
            ret = {"type_list": self.game_data.hu_manager.check_hu_result(hand_card)}
        return ret

    def can_ting(self, hand_card):
        # 如果听牌则不重复判断, 直接返回空字典
        if self.game_data.state_machine.players[self.seat_id].hand_card.is_ting:
            return {}
        ting_info = self.game_data.hu_manager.check_ting_result(hand_card)
        self.players[self.seat_id].set_can_ting_info(ting_info)
        return ting_info
