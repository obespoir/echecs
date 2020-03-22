# coding=utf-8
import time

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.models.card.hand_card import HandCard
from service.mahjong.models.utils.cardanalyse import CardAnalyse


class DanGouJiang(BaseType):
    """
    8)	单钓将：胡牌时，钓单张牌做将成胡。
    """

    def __init__(self):
        super(DanGouJiang, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        hu_card_val = hand_card.hu_card_val
        j, s, k = card_analyse.get_jiang_ke_shun(hand_card.hand_card_vals)
        print("j=", j)
        if hu_card_val and hu_card_val in j[0]:
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
        1: [11, 3, 0, 0, 1, 1, 1, 2, 0, 3],  # 万
        2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
        3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
        4: [0, 0, 0, 0, 0],  # 风
        5: [3, 3, 0, 0],  # 箭
    }
    # hand_card.chi_card_vals=[[23,24,25]]
    hand_card.handle_hand_card_for_settle_show()
    hand_card.union_hand_card()
    hand_card.hu_card_val = 23
    print("hand_card =", hand_card.hand_card_vals)
    test_type = DanGouJiang()
    start_time = time.time()
    print(test_type.is_this_type(hand_card, card_analyse))
    print("time = ", time.time() - start_time)
