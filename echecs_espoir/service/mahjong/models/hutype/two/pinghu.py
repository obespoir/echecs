# coding=utf-8
import time

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType, CARD_SIZE
from service.mahjong.models.card.hand_card import HandCard
from service.mahjong.models.utils.cardanalyse import CardAnalyse


class PingHu(BaseType):
    """
    3)	平胡：胡牌时，牌型由4副顺子及序数牌作将组成。边、坎、钓不影响平胡。
    """

    def __init__(self):
        super(PingHu, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        used_card_type = [CardType.WAN]  # 此游戏中使用的花色
        union_card = hand_card.union_card_info
        if union_card[CardType.WAN][0] != 14:
            return False
        j, s, k = card_analyse.get_jiang_ke_shun(hand_card.hand_card_vals)
        # 4,5,6 至少有一张
        s.extend(hand_card.chi_card_vals)
        return len(s) == 4


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
        1: [9, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 万
        2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
        3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
        4: [2, 2, 0, 0, 0],                 # 风
        5: [0, 0, 0, 0],                    # 箭
    }
    hand_card.chi_card_vals=[[23,24,25]]
    hand_card.handle_hand_card_for_settle_show()
    hand_card.union_hand_card()
    print("hand_card =", hand_card.hand_card_vals)
    test_type = PingHu()
    start_time = time.time()
    print(test_type.is_this_type(hand_card, card_analyse))
    print("time = ", time.time() - start_time)