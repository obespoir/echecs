# coding=utf-8
import time
import copy
from collections import Counter

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType, CARD_SIZE
from service.mahjong.models.card.hand_card import HandCard
from service.mahjong.models.card.card import Card
from service.mahjong.models.utils.cardanalyse import CardAnalyse


class HuJueZhang(BaseType):
    """
    4)	胡绝张：胡牌时，胡牌池、桌面已亮明的3张牌所剩的第4张牌。（抢杠胡不计胡绝张）
    """

    def __init__(self):
        super(HuJueZhang, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        used_card_type = [CardType.WAN]  # 此游戏中使用的花色
        hu_card_val = hand_card.hu_card_val
        cards = hand_card.hand_card_vals
        tmp_cards = copy.deepcopy(hand_card.game_data.yi_chu_card_vals)
        tmp_cards.extend(cards)
        print("HuJueZhang tmp_cards=", tmp_cards)
        ret = Counter(tmp_cards)

        return ret.get(hu_card_val) == 3



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
        1: [14, 4, 4, 4, 0, 0, 0, 0, 0, 2],  # 万
        2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
        3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
        4: [0, 0, 0, 0, 0],                 # 风
        5: [0, 0, 0, 0],                    # 箭

    }
    hand_card.handle_hand_card_for_settle_show()
    hand_card.union_hand_card()
    print("hand_card =", hand_card.hand_card_vals)
    test_type = HuJueZhang()
    start_time = time.time()
    print(test_type.is_this_type(hand_card, card_analyse))
    print("time = ", time.time() - start_time)