# coding=utf-8
import time

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType, CARD_SIZE
from service.mahjong.models.card.hand_card import HandCard
from service.mahjong.models.card.card import Card
from service.mahjong.models.utils.cardanalyse import CardAnalyse


class HunYaoJiu(BaseType):
    """
    3)	混幺九：胡牌时，由字牌和序数牌一、九的刻子及将牌组成的牌型。
    不记番： 碰碰和、幺九刻、全带幺
    """

    def __init__(self):
        super(HunYaoJiu, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        used_card_type = [CardType.WAN]  # 此游戏中使用的花色
        union_card = hand_card.union_card_info
        for index, count in enumerate(union_card[CardType.WAN]):
            if index in [0, 1, 9]:
                continue
            if count > 0:
                return False
        return True



if __name__ == "__main__":
    pass
    card_analyse = CardAnalyse()
    hand_card = HandCard(0, None)
    # hand_card.hand_card_info = {
    #     1: [9, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 万
    #     2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
    #     3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
    #     4: [2, 2, 0, 0, 0],                 # 风
    #     5: [3, 3, 0, 0],                    # 箭
    # }
    hand_card.hand_card_info = {
        1: [11, 0, 1, 1, 1, 1, 2, 2, 1, 2],  # 万
        2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
        3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
        4: [3, 0, 0, 3, 0],                 # 风
        5: [0, 0, 0, 0],                    # 箭

    }
    # hand_card.record_peng_card(67)
    hand_card.handle_hand_card_for_settle_show()
    print("hand_card =", hand_card.hand_card_vals)
    test_type = HunYaoJiu()
    start_time = time.time()
    print(test_type.is_this_type(hand_card, card_analyse))
    print("time = ", time.time() - start_time)