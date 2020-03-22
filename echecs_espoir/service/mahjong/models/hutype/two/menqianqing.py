# coding=utf-8
import time

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType, CARD_SIZE
from service.mahjong.models.card.hand_card import HandCard
from service.mahjong.models.utils.cardanalyse import CardAnalyse


class MenQianQing(BaseType):
    """
    2)	门前清：胡牌时，除了胡的那张牌是别人打出来的，其他的牌都是自己抓的。
    """

    def __init__(self):
        super(MenQianQing, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        used_card_type = [CardType.WAN]  # 此游戏中使用的花色
        hand_card_for_settle_show = hand_card.hand_card_for_settle_show

        return len(hand_card_for_settle_show) == 2


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
    hand_card.record_chi_card(23, [24, 25])
    hand_card.handle_hand_card_for_settle_show()
    hand_card.union_hand_card()
    print("hand_card =", hand_card.hand_card_vals)
    test_type = MenQianQing()
    start_time = time.time()
    print(test_type.is_this_type(hand_card, card_analyse))
    print("time = ", time.time() - start_time)