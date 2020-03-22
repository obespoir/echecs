# coding=utf-8
import time

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType
from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType, CARD_SIZE
from service.mahjong.models.card.hand_card import HandCard
from service.mahjong.models.utils.cardanalyse import CardAnalyse


class PengPengHu(BaseType):
    """
    1)	碰碰胡: 胡牌时，牌型由4副刻子（或杠）、将牌组成。
    """
    def __init__(self):
        super(PengPengHu, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        chi_cards = hand_card.chi_card_vals
        if chi_cards:
            return False
        j, s, k = card_analyse.get_jiang_ke_shun(hand_card.hand_card_vals)
        if hand_card.peng_card_vals:
            for peng_group in hand_card.chi_card_vals:
                k.append(peng_group)
        if hand_card.bu_gang_card_vals:
            for group in hand_card.bu_gang_card_vals:
                k.append([group[0], group[0], group[0]])
        if hand_card.an_gang_card_vals:
            for group in hand_card.an_gang_card_vals:
                k.append([group[0], group[0], group[0]])
        if hand_card.dian_gang_card_vals:
            for group in hand_card.dian_gang_card_vals:
                k.append([group[0], group[0], group[0]])

        return len(k) == 4

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
        1: [14, 0, 3, 3, 3, 2, 3, 0, 0, 0],  # 万
        2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
        3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
        4: [0, 0, 0, 0, 0],                 # 风
        5: [0, 0, 0, 0],                    # 箭
    }

    hand_card.handle_hand_card_for_settle_show()
    hand_card.union_hand_card()
    print("hand_card =", hand_card.hand_card_vals)
    test_type = PengPengHu()
    start_time = time.time()
    print(test_type.is_this_type(hand_card, card_analyse, None))
    print("time = ", time.time() - start_time)