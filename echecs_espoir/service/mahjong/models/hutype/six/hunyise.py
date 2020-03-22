# coding=utf-8
import time

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.models.card.hand_card import HandCard
from service.mahjong.models.utils.cardanalyse import CardAnalyse

class HunYiSe(BaseType):
    """
    1)	混一色: 胡牌时，牌型由一种花色序数牌及字牌组成。
    """
    def __init__(self):
        super(HunYiSe, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        # TODO 还有不是混一色的吗?
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
        1: [14, 0, 3, 3, 3, 2, 3, 0, 0, 0],  # 万
        2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
        3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
        4: [0, 0, 0, 0, 0],                 # 风
        5: [0, 0, 0, 0],                    # 箭
    }

    hand_card.handle_hand_card_for_settle_show()
    hand_card.union_hand_card()
    print("hand_card =", hand_card.hand_card_vals)
    test_type = HunYiSe()
    start_time = time.time()
    print(test_type.is_this_type(hand_card, card_analyse))
    print("time = ", time.time() - start_time)