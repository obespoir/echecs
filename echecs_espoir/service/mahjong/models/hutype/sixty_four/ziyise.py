# coding=utf-8
import time

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType, CARD_SIZE
from service.mahjong.models.card.hand_card import HandCard
from service.mahjong.models.card.card import Card
from service.mahjong.models.utils.cardanalyse import CardAnalyse


class ZiYiSe(BaseType):
    """
    4)	字一色：胡牌时，牌型由字牌的刻子（杠）、将组成
    不记番：碰碰和、混幺九、全带幺、幺九刻、三风刻
    """

    def __init__(self):
        super(ZiYiSe, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        used_card_type = [CardType.WAN]  # 此游戏中使用的花色
        union_card = hand_card.union_card_info
        return union_card[CardType.FENG][0] + union_card[CardType.JIAN][0] == 14



if __name__ == "__main__":
    pass
    card_analyse = CardAnalyse()
    hand_card = HandCard(0, None)
    hand_card.hand_card_info = {
        1: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 万
        2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
        3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
        4: [8, 2, 3, 3, 0],                 # 风
        5: [6, 3, 3, 0],                    # 箭
    }
    # hand_card.hand_card_info = {
    #     1: [14, 4, 4, 4, 0, 0, 0, 0, 0, 2],  # 万
    #     2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
    #     3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
    #     4: [0, 0, 0, 0, 0],                 # 风
    #     5: [0, 0, 0, 0],                    # 箭
    #
    # }
    hand_card.handle_hand_card_for_settle_show()
    hand_card.union_hand_card()
    print("hand_card =", hand_card.hand_card_vals)
    test_type = ZiYiSe()
    start_time = time.time()
    print(test_type.is_this_type(hand_card, card_analyse))
    print("time = ", time.time() - start_time)