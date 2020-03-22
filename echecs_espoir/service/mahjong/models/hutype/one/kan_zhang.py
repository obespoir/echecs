# coding=utf-8
import time
import copy

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType, CARD_SIZE
from service.mahjong.models.card.hand_card import HandCard
from service.mahjong.models.utils.cardanalyse import CardAnalyse


class KanZhang(BaseType):
    """
    7)	坎张：   胡牌时，和2张牌之间的牌。4556和5也为坎张，手中有45567和6不算坎张。因为后者胡的6可以是456里的6。
    """

    def __init__(self):
        super(KanZhang, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        hu_card_val = hand_card.hu_card_val
        chi_cards_lst = hand_card.chi_card_vals
        ret = card_analyse.get_jiang_ke_shun_plus(hand_card.hand_card_vals)
        for index in range(len(ret)):
            s = ret[index]["s"]
            s.extend(chi_cards_lst)
            for i in s:
                if hu_card_val == i[1]:
                    return True
        return False


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
        1: [6, 0, 0, 0, 1, 1, 1, 1, 1, 1],  # 万
        2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
        3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
        4: [2, 2, 0, 0, 0],                 # 风
        5: [3, 3, 0, 0],                    # 箭
    }
    hand_card.chi_card_vals=[[23,24,25]]
    hand_card.handle_hand_card_for_settle_show()
    hand_card.union_hand_card()
    hand_card.hu_card_val = 24
    print("hand_card =", hand_card.hand_card_vals)
    test_type = KanZhang()
    start_time = time.time()
    for i in range(100):
        r = test_type.is_this_type(hand_card, card_analyse)
    print("time = ", (time.time() - start_time) / 100)
    print(r)