# coding=utf-8
import copy
import time

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType
from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType, CARD_SIZE
from service.mahjong.models.card.hand_card import HandCard
from service.mahjong.models.utils.cardanalyse import CardAnalyse


class TianHu(BaseType):
    """
    6)	天胡 :庄家在发完牌就胡牌。如果庄家有补花，在补完花后就胡牌也算。如果庄家在发完牌后有暗杠，那么不算天胡。
    不记番：边张,坎张,单钓将,不求人,胡绝张,自摸
    """
    def __init__(self):
        super(TianHu, self).__init__()

    def is_this_type(self, hand_card, card_analyse):

        return bool(hand_card.is_tian_hu)


if __name__ == "__main__":
    pass
    card_analyse = CardAnalyse()
    hand_card = HandCard(0, None)
    # hand_card.hand_card_info = {
    #     1: [14, 3, 3, 3, 1, 1, 1, 0, 0, 2],  # 万
    #     2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
    #     3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
    #     4: [0, 0, 0, 0, 0],                 # 风
    #     5: [0, 0, 0, 0],                    # 箭
    # }
    hand_card.hand_card_info = {
        1: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 万
        2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
        3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
        4: [6, 3, 3, 0, 0],                 # 风
        5: [8, 3, 3, 2],                    # 箭
    }

    hand_card.handle_hand_card_for_settle_show()
    hand_card.union_hand_card()
    print("hand_card =", hand_card.hand_card_vals)
    test_type = TianHu()
    start_time = time.time()
    print(test_type.is_this_type(hand_card, card_analyse))
    print("time = ", time.time() - start_time)