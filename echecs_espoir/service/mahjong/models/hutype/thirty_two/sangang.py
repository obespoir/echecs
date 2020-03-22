# coding=utf-8
import time

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType
from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType, CARD_SIZE
from service.mahjong.models.card.hand_card import HandCard
from service.mahjong.models.utils.cardanalyse import CardAnalyse


class SanGang(BaseType):
    """
    1)	三杠: 胡牌时，牌里有3副杠，明暗杠均可 不记番： 双明杠、双暗杠、明杠、暗杠
    """
    def __init__(self):
        super(SanGang, self).__init__()



    def is_this_type(self, hand_card, card_analyse):
        an_gang_card_vals = hand_card.an_gang_card_vals
        bu_gang_card_vals = hand_card.bu_gang_card_vals
        dian_gang_card_vals = hand_card.dian_gang_card_vals
        ke_lst = []
        ke_lst.extend(an_gang_card_vals)
        ke_lst.extend(bu_gang_card_vals)
        ke_lst.extend(dian_gang_card_vals)

        return len(ke_lst) == 3

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
        1: [4, 0, 0, 0, 0, 0, 0, 0, 0, 3],  # 万
        2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
        3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
        4: [0, 0, 0, 0, 0],                 # 风
        5: [2, 2, 0, 0],                    # 箭
    }

    hand_card.handle_hand_card_for_settle_show()
    hand_card.union_hand_card()
    hand_card.record_peng_card(20)
    hand_card.record_dian_gang_card(0, 17)
    hand_card.record_an_gang_card(18)
    hand_card.record_bu_gang_card(20)
    print("hand_card =", hand_card.hand_card_vals)
    test_type = SanGang()
    start_time = time.time()
    print(test_type.is_this_type(hand_card, card_analyse))
    print("time = ", time.time() - start_time)