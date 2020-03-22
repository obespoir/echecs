# coding=utf-8
import time

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType
from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType, CARD_SIZE
from service.mahjong.models.card.hand_card import HandCard
from service.mahjong.models.utils.cardanalyse import CardAnalyse


class QuanQiuRen(BaseType):
    """
    3)	全求人: 胡牌时，全靠吃牌、碰牌、单钓别人打出的牌胡牌。不记番：单钓
    """
    def __init__(self):
        super(QuanQiuRen, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        cards = hand_card.hand_card_vals
        return len(cards) == 2

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
        1: [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],  # 万
        2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
        3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
        4: [0, 0, 0, 0, 0],                 # 风
        5: [0, 0, 0, 0],                    # 箭
    }

    hand_card.handle_hand_card_for_settle_show()
    hand_card.union_hand_card()
    hand_card.record_peng_card(17)
    hand_card.record_peng_card(18)
    hand_card.record_peng_card(19)
    print("hand_card =", hand_card.hand_card_vals)
    test_type = QuanQiuRen()
    start_time = time.time()
    print(test_type.is_this_type(hand_card, card_analyse, None))
    print("time = ", time.time() - start_time)