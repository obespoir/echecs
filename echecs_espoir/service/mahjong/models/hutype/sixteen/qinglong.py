# coding=utf-8
import copy
import time

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.models.card.hand_card import HandCard
from service.mahjong.models.utils.cardanalyse import CardAnalyse


class QingLong(BaseType):
    """
    1)	清龙: 清龙，指同花色的一条龙，国标麻将的番种之一。是指和牌时，有一种相同花色的123，456，789三副顺子。
        清龙不要求必定的清一色，所以清龙不是清一色一条龙的简称。
    不记番： 连6、老少副
    """
    def __init__(self):
        super(QingLong, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        wan = [[17, 18, 19], [20, 21, 22], [23, 24, 25]]  # TODO 可扩展为全牌型
        chi_card_vals = hand_card.chi_card_vals
        ret = card_analyse.get_jiang_ke_shun_plus(hand_card.hand_card_vals)
        for index in range(len(ret)):

            s = ret[index]["s"]
            s.extend(chi_card_vals)
            if wan[0] in s and wan[1] in s and wan[2] in s:
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
        1: [14, 3, 1, 3, 1, 1, 1, 1, 1, 2],  # 万
        2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
        3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
        4: [0, 0, 0, 0, 0],                 # 风
        5: [0, 0, 0, 0],                    # 箭
    }

    hand_card.handle_hand_card_for_settle_show()
    hand_card.union_hand_card()
    print("hand_card =", hand_card.hand_card_vals)
    test_type = QingLong()
    start_time = time.time()
    print(test_type.is_this_type(hand_card, card_analyse))
    print("time = ", time.time() - start_time)