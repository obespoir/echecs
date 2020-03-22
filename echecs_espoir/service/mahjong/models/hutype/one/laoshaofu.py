# coding=utf-8
import time

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType, CARD_SIZE
from service.mahjong.models.card.hand_card import HandCard
from service.mahjong.models.utils.cardanalyse import CardAnalyse


class LaoShaoFu(BaseType):
    """
    3)	老少副：胡牌时，手上有花色相同的123、789的顺子。
    """

    def __init__(self):
        super(LaoShaoFu, self).__init__()

    def is_this_type(self, hand_card, card_analyse):

        j, s, k = card_analyse.get_jiang_ke_shun(hand_card.hand_card_vals)
        if hand_card.chi_card_vals:
            s.extend(hand_card.chi_card_vals)
        if len(s) < 2:
            return False
        s.sort()
        print("s=", s)
        if [17,18,19] in s and [23, 24, 25] in s:
            return True
        return False


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
        1: [6, 0, 0, 0, 1, 1, 1, 1, 1, 1],  # 万
        2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
        3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
        4: [2, 2, 0, 0, 0],                 # 风
        5: [3, 3, 0, 0],                    # 箭
    }
    # hand_card.chi_card_vals=[[23,24,25]]
    hand_card.chi_card_vals=[[17,18,19]]
    hand_card.handle_hand_card_for_settle_show()
    hand_card.union_hand_card()
    print("hand_card =", hand_card.hand_card_vals)
    test_type = LaoShaoFu()
    start_time = time.time()
    print(test_type.is_this_type(hand_card, card_analyse))
    print("time = ", time.time() - start_time)