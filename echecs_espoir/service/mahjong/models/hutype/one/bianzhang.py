# coding=utf-8
import time
import copy

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType, CARD_SIZE
from service.mahjong.models.card.hand_card import HandCard
from service.mahjong.models.utils.cardanalyse import CardAnalyse


class BianZhang(BaseType):
    """
    6)	边张：   胡牌时，单胡一张牌，并且是顺子，123的3或789的7；其中1233胡3,7789胡7都是边张。
                但是12345胡3,56789胡7不算边张，因为能胡两张以上的牌。
    """

    def __init__(self):
        super(BianZhang, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        hu_card_val = hand_card.hu_card_val
        if not hu_card_val and hu_card_val not in [19, 23]:
            return False

        ret = card_analyse.get_jiang_ke_shun_plus(hand_card.hand_card_vals)
        for index in range(len(ret)):

            s = ret[index]["s"]
            if len(s) < 1:
                return False
            if [17, 18, 19] in s:
                return True
            if [23, 24, 25] in s:
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
    hand_card.chi_card_vals=[[23,24,25]]
    hand_card.handle_hand_card_for_settle_show()
    hand_card.union_hand_card()
    hand_card.hu_card_val = 23
    print("hand_card =", hand_card.hand_card_vals)
    test_type = BianZhang()
    start_time = time.time()
    for i in range(100):
        r = test_type.is_this_type(hand_card, card_analyse)
    print("time = ", (time.time() - start_time) / 100)
    print(r)