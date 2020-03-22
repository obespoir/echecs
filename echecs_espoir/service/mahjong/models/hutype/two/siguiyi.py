# coding=utf-8
import time

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType, CARD_SIZE
from service.mahjong.models.card.hand_card import HandCard
from service.mahjong.models.card.card import Card
from service.mahjong.models.utils.cardanalyse import CardAnalyse


class SiGuiYi(BaseType):
    """
    4)	四归一：胡牌时，牌里有4张相同的牌归于一家的顺、刻子、对、将牌中（不包括杠牌） 。
    """

    def __init__(self):
        super(SiGuiYi, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        used_card_type = [CardType.WAN]  # 此游戏中使用的花色
        union_card = hand_card.union_card_info
        gang_lst = []
        gang_lst.extend(hand_card.dian_gang_card_vals)
        gang_lst.extend(hand_card.bu_gang_card_vals)
        gang_lst.extend(hand_card.an_gang_card_vals)
        ret = []  # 手里有4张的牌集
        for i, count in enumerate(union_card[CardType.WAN]):
            if i == 0 and count < 4:
                return False
            if count == 4 and Card.cal_card_val(CardType.WAN, i) not in gang_lst:
                ret.append(Card.cal_card_val(CardType.WAN, i))
        if not ret:
            return False
        gang_lst = self.get_gang_lst(hand_card)
        for i in ret:
            if i in gang_lst:
                return False
        return True

    def get_gang_lst(self, hand_card):
        ret = []
        for i in hand_card.dian_gang_card_vals: # 点杠的牌
            ret.append(i[0])
        for i in hand_card.bu_gang_card_vals:  # 补杠的牌
            ret.append(i[0])
        for i in hand_card.an_gang_card_vals:  # 暗杠的牌
            ret.append(i[0])
        return ret

if __name__ == "__main__":
    pass
    card_analyse = CardAnalyse()
    hand_card = HandCard(0)
    # hand_card.hand_card_info = {
    #     1: [9, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 万
    #     2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
    #     3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
    #     4: [2, 2, 0, 0, 0],                 # 风
    #     5: [3, 3, 0, 0],                    # 箭
    # }
    hand_card.hand_card_info = {
        1: [9, 1, 1, 4, 1, 1, 1, 1, 1, 1],  # 万
        2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
        3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
        4: [2, 2, 0, 0, 0],                 # 风
        5: [0, 0, 0, 0],                    # 箭

    }
    hand_card.handle_hand_card_for_settle_show()
    hand_card.union_hand_card()
    print("hand_card =", hand_card.hand_card_vals)
    test_type = SiGuiYi()
    start_time = time.time()
    print(test_type.is_this_type(hand_card, card_analyse))
    print("time = ", time.time() - start_time)