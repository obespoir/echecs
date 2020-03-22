# coding=utf-8
import copy
import time

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType
from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType, CARD_SIZE
from service.mahjong.models.card.hand_card import HandCard
from service.mahjong.models.utils.cardanalyse import CardAnalyse


class YiSeSanBuGao(BaseType):
    """
    2)	一色三步高 : 胡牌时，牌里有一种花色的牌，依次递增一位或依次递增二位数字的3副顺子。
    """
    def __init__(self):
        super(YiSeSanBuGao, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        chi_card_vals = hand_card.chi_card_vals
        ret = card_analyse.get_jiang_ke_shun_plus(hand_card.hand_card_vals)
        for index in range(len(ret)):

            s = ret[index]["s"]
            s.extend(chi_card_vals)
            if len(s) < 3:
                return False
            s.sort()
            if s[0][1] == s[1][0] and s[0][2] == s[2][0]:
                return True
            if s[0][2] == s[1][0] and s[1][2] == s[2][2]:
                return True
            if len(s) == 4:
                if s[1][1] == s[2][0] and s[1][2] == s[3][0]:
                    return True
                if s[1][2] == s[2][0] and s[2][2] == s[3][2]:
                    return True
            print(s)

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
        1: [12, 2, 2, 2, 2, 2, 2, 0, 0, 0],  # 万
        2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
        3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
        4: [0, 0, 0, 0, 0],                 # 风
        5: [2, 2, 0, 0],                    # 箭
    }

    hand_card.handle_hand_card_for_settle_show()
    hand_card.union_hand_card()
    print("hand_card =", hand_card.hand_card_vals)
    test_type = YiSeSanBuGao()
    start_time = time.time()
    print(test_type.is_this_type(hand_card, card_analyse))
    print("time = ", time.time() - start_time)