# coding=utf-8
import copy
import time

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType
from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType, CARD_SIZE
from service.mahjong.models.card.hand_card import HandCard
from service.mahjong.models.utils.cardanalyse import CardAnalyse


class DaSanYuan(BaseType):
    """
    2)	大三元 :胡牌时，牌里有中、发、白3副刻子
    不记番： 箭刻、双箭刻、幺九刻
    """
    def __init__(self):
        super(DaSanYuan, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        # 不是清一色则返 False
        union_card = hand_card.union_card_info
        # 4,5,6 至少有一张
        if union_card[CardType.JIAN][0] == 9:
            return True
        return False


if __name__ == "__main__":
    pass
    card_analyse = CardAnalyse()
    hand_card = HandCard(0, None)
    hand_card.hand_card_info = {
        1: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 万
        2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
        3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
        4: [5, 3, 2, 0, 0],                 # 风
        5: [9, 3, 3, 3],                    # 箭
    }
    # hand_card.hand_card_info = {
    #     1: [8, 0, 0, 0, 1, 2, 2, 1, 0, 2],  # 万
    #     2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
    #     3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
    #     4: [0, 0, 0, 0, 0],                 # 风
    #     5: [0, 0, 0, 0],                    # 箭
    # }

    # hand_card.record_chi_card(19,[17,18])
    # hand_card.record_peng_card(83)
    hand_card.handle_hand_card_for_settle_show()
    print("hand_card =", hand_card.hand_card_vals)
    test_type = DaSanYuan()
    start_time = time.time()
    print(test_type.is_this_type(hand_card, card_analyse))
    print("time = ", time.time() - start_time)