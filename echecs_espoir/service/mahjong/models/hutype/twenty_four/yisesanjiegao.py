# coding=utf-8
import copy
import time

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType
from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType, CARD_SIZE
from service.mahjong.models.card.hand_card import HandCard
from service.mahjong.models.utils.cardanalyse import CardAnalyse


class YiSeSanJieGao(BaseType):
    """
    4)	一色三节高 :胡牌时，牌里有一种花色且依次递增一位数字的3副刻子
    不记番：一色三同顺
    """
    def __init__(self):
        super(YiSeSanJieGao, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        peng_cards = hand_card.peng_card_vals
        an_gang_card_vals = hand_card.an_gang_card_vals
        bu_gang_card_vals = hand_card.bu_gang_card_vals
        dian_gang_card_vals = hand_card.dian_gang_card_vals
        ke_lst = []
        ke_lst.extend(peng_cards)
        ke_lst.extend(an_gang_card_vals)
        ke_lst.extend(bu_gang_card_vals)
        ke_lst.extend(dian_gang_card_vals)
        ret = card_analyse.get_jiang_ke_shun_plus(hand_card.hand_card_vals)
        for index in range(len(ret)):

            k = ret[index]["k"]
            k.extend(ke_lst)
            print("k=", k)
            if len(k) < 3:
                return False
            if k[0][0]-1 == k[1][0] and k[1][0]-1 == k[2][0]:
                return True
            if len(k) == 4:
                if k[1][0] - 1 == k[2][0] and k[2][0] - 1 == k[3][0]:
                    return True
        return False


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
        1: [7, 3, 0, 0, 0, 1, 0, 1, 2, 0],  # 万
        2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
        3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
        4: [0, 0, 0, 0, 0],                 # 风
        5: [0, 0, 0, 0],                    # 箭
    }

    hand_card.record_peng_card(82)
    hand_card.record_chi_card(18, [19, 20])
    hand_card.handle_hand_card_for_settle_show()
    hand_card.union_hand_card()
    print("hand_card =", hand_card.hand_card_vals)
    test_type = YiSeSanJieGao()
    start_time = time.time()
    print(test_type.is_this_type(hand_card, card_analyse))
    print("time = ", time.time() - start_time)