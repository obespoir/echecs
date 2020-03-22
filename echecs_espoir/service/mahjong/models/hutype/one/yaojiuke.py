# coding=utf-8
import time

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType, CARD_SIZE
from service.mahjong.models.card.hand_card import HandCard
from service.mahjong.models.utils.cardanalyse import CardAnalyse


class YaoJiuKe(BaseType):
    """
    4)	幺九刻：胡牌时，手上有一副1万或9万或字牌的刻子或杠。
    """

    def __init__(self):
        super(YaoJiuKe, self).__init__()

    def is_this_type(self, hand_card, card_analyse):

        j, s, k = card_analyse.get_jiang_ke_shun(hand_card.hand_card_vals)
        print("k=", k)
        if hand_card.peng_card_vals:
            k.extend(hand_card.peng_card_vals)
        if len(k) < 2:
            return False
        print("k=", k)
        if [17, 17, 17] in k and [25, 25, 25] in k:
            return True
        for i in [65, 66, 67, 68]:
            if i in k:
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
        1: [8, 0, 0, 0, 1, 1, 1, 2, 0, 3],  # 万
        2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
        3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
        4: [0, 0, 0, 0, 0],                 # 风
        5: [3, 3, 0, 0],                    # 箭
    }
    # hand_card.chi_card_vals=[[23,24,25]]
    hand_card.peng_card_vals=[[17,17,17]]
    hand_card.handle_hand_card_for_settle_show()
    hand_card.union_hand_card()
    print("hand_card =", hand_card.hand_card_vals)
    test_type = YaoJiuKe()
    start_time = time.time()
    print(test_type.is_this_type(hand_card, card_analyse))
    print("time = ", time.time() - start_time)