# coding=utf-8

import copy

from share import message_ids
from service.mahjong.constants.carddefine import BLACK
from service.mahjong.controls.notifybridge import notify_single_user
from service.mahjong.models.systemact.base_system_act import BaseSystemAct
from service.mahjong.constants.carddefine import CardType
from service.mahjong.models.card.card import Card
from service.mahjong.constants.gamedefine import Act
from service.mahjong.models.callbackmanager import CallbackFuncType
from config.globalconfig import GlobalConfig

from obespoir.share.ob_log import logger


class DealCard(BaseSystemAct):
    """
    初始发牌
    """
    def __init__(self, game_data):
        super(DealCard, self).__init__(game_data=game_data)

    def execute(self):
        """
        初始发牌
        :return:
        """
        logger.debug(u"初始发牌: %s", str([]))
        card_results = []
        for i in range(self.max_player_num):
            drew_card_vals = self.card_dealer.draw_cards(num=13)
            # 处理测试初始化发牌
            if GlobalConfig().test_sure_next_cards.get(self.desk_id):
                test_cards = GlobalConfig().test_sure_next_cards[self.desk_id][i]
                if test_cards:
                    min_len = min(len(test_cards),len(drew_card_vals))
                    for index in range(min_len):
                        drew_card_vals[index] = test_cards[index]
            # 测试初始化发牌结束
            card_results.append(drew_card_vals)




        for x in self.players:
            result = []
            for y in self.players:
                if x.seat_id == y.seat_id:
                    data = {"seat_id": y.seat_id, "card_list": card_results[y.seat_id]}
                else:
                    data = {"seat_id": y.seat_id, "card_list": [BLACK]*13}
                result.append(data)
            notify_single_user(self.desk_id, x.seat_id, message_ids.PUSH_DEAL_CARD, data={"card_list": result})
        for x in self.players:
            if self.game_config.draw_card_bu_hua:
                self.bu_hua(x.seat_id, card_results[x.seat_id])
            # 发牌时候同时将牌添加入手牌
            print("card_results[%s] = %s len=%s" % (x.seat_id, card_results[x.seat_id], len(card_results[x.seat_id])))
            self.players[x.seat_id].hand_card.add_hand_card_by_vals(card_results[x.seat_id])
        # 添加玩家动作, Waite_answer
        # for i in range(self.game_data.max_player_num):
        #     self.game_data.add_player_to_act(i, Act.WAITE_ANSWER)
        # 添加超时回调
        self.game_data.next_speaker_callback = {"type": CallbackFuncType.FUNC_NOTIFY_PLAYER_ACT, "call_params": {
            "seat_id": self.game_data.banker_seat_id,
            "interval": self.get_act_wait_time(self.game_data.banker_seat_id, Act.WAITE_ANSWER),
            "act_info": {}}}
        return 1

    def bu_hua(self, seat_id, card_list=[]):
        """检查是否补花"""
        hua_card = []
        tmp_card_list = copy.deepcopy(card_list)
        for c in tmp_card_list:
            if CardType.HUA == Card.cal_card_type(c):
                hua_card.append(c)
                card_list.remove(c)
        if not hua_card:
            return 0
        logger.debug('发牌补花：%d', len(hua_card))
        new_cards = []
        temp_hua = copy.deepcopy(hua_card)
        while temp_hua:
            cards = self.card_dealer.draw_cards(num=len(temp_hua), is_last=True)
            temp_hua = []
            for c in cards:
                if CardType.HUA == Card.cal_card_type(c):
                    temp_hua.append(c)
                    hua_card.append(c)
                else:
                    new_cards.append(c)
        card_list.extend(new_cards)
        # 将补花数量添加进手牌中 hua_card_vals 中
        self.players[seat_id].hand_card.hua_card_vals.extend(hua_card)
        for p in self.players:
            if p.seat_id == seat_id:
                notify_single_user(self.desk_id, p.seat_id, message_ids.PUSH_GAME_DEAL_BU_HUA,
                                   data={"seat_id": seat_id, "hua_card": hua_card, "bu_cards": new_cards})
            else:
                notify_single_user(self.desk_id, p.seat_id, message_ids.PUSH_GAME_DEAL_BU_HUA,
                                   data={"seat_id": seat_id, "hua_card": hua_card, "bu_cards": [BLACK]*len(new_cards)})
        return 1
