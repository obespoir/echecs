# coding=utf-8
import copy
import time

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType
from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType, CARD_SIZE
from service.mahjong.models.card.hand_card import HandCard
from service.mahjong.models.utils.cardanalyse import CardAnalyse


class QiLianDui(BaseType):
    """
    5)	七连对 :胡牌时，由一种花色序数牌且序数相连的7个对子组成 。
    不记番： 清一色、不求人、单钓、门清、七对
    """
    def __init__(self):
        super(QiLianDui, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        # 不是清一色则返 False
        union_card = hand_card.union_card_info
        # 4,5,6 至少有一张
        if union_card[CardType.WAN][0] != 14:
            return False
        if union_card[CardType.WAN][1] == 2:
            dui_count = 0
            for index, count in enumerate(union_card[CardType.WAN][:-2]):
                if count == 2:
                    dui_count += 1
            if dui_count == 7:
                return True

        if union_card[CardType.WAN][1] == 0 and union_card[CardType.WAN][9] == 0:
            dui_count = 0
            for index, count in enumerate(union_card[CardType.WAN][1:-1]):
                if count == 2:
                    dui_count += 1
            if dui_count == 7:
                return True

        if union_card[CardType.WAN][1] == 0 and union_card[CardType.WAN][2] == 0:
            dui_count = 0
            for index, count in enumerate(union_card[CardType.WAN][1:-1]):
                if count == 2:
                    dui_count += 1
            if dui_count == 7:
                return True
        return False


if __name__ == "__main__":
    pass
    card_analyse = CardAnalyse()
    hand_card = HandCard(0, None)
    hand_card.hand_card_info = {
        1: [14, 2, 2, 2, 2, 2, 2, 2, 0, 0],  # 万
        2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
        3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
        4: [0, 0, 0, 0, 0],                 # 风
        5: [0, 0, 0, 0],                    # 箭
    }
    # hand_card.hand_card_info = {
    #     1: [14, 3, 1, 1, 1, 1, 1, 1, 2, 3],  # 万
    #     2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
    #     3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
    #     4: [0, 0, 0, 0, 0],                 # 风
    #     5: [0, 0, 0, 0],                    # 箭
    # }

    hand_card.handle_hand_card_for_settle_show()
    hand_card.union_hand_card()
    print("hand_card =", hand_card.hand_card_vals)
    test_type = QiLianDui()
    start_time = time.time()
    print(test_type.is_this_type(hand_card, card_analyse))
    print("time = ", time.time() - start_time)