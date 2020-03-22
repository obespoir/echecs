# coding=utf-8
import time

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType
from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType, CARD_SIZE
from service.mahjong.models.card.hand_card import HandCard
from service.mahjong.models.utils.cardanalyse import CardAnalyse


class SanFengKe(BaseType):
    """
    1)	三风刻: 胡牌时，牌里有3个风刻（杠）
    不记番：箭刻
    """
    def __init__(self):
        super(SanFengKe, self).__init__()


    def is_feng(self, i):
        if i:
            return i[0] in [65, 66, 67, 68]
        else:
            return False

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
        feng_ke_count = 0
        ret = card_analyse.get_jiang_ke_shun_plus(hand_card.hand_card_vals)
        for index in range(len(ret)):
            k = ret[index]["k"]
            ke_lst.extend(k)
            for i in k:
                if self.is_feng(i):
                    feng_ke_count += 1
            if feng_ke_count >= 3:
                return True
        return False

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
        1: [5, 0, 3, 0, 2, 0, 0, 0, 0, 0],  # 万
        2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
        3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
        4: [9, 3, 3, 3, 0],                 # 风
        5: [0, 0, 0, 0],                    # 箭
    }

    hand_card.handle_hand_card_for_settle_show()
    hand_card.union_hand_card()
    print("hand_card =", hand_card.hand_card_vals)
    test_type = SanFengKe()
    start_time = time.time()
    print(test_type.is_this_type(hand_card, card_analyse))
    print("time = ", time.time() - start_time)