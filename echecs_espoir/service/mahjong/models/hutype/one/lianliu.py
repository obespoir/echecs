# coding=utf-8
import time

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType, CARD_SIZE
from service.mahjong.models.card.hand_card import HandCard
from service.mahjong.models.utils.cardanalyse import CardAnalyse


class LianLiu(BaseType):
    """
    2)	连六：胡牌时，手上有6张序数相连的顺子。（123,456）
    """

    def __init__(self):
        super(LianLiu, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        used_card_type = [CardType.WAN]  # 此游戏中使用的花色
        # # 4,5,6 至少有一张
        # for t in CardType.all_type():
        #     if t in used_card_type:
        #         for i in range(CARD_SIZE[t]):
        #             if i in [4, 5, 6]:
        #                 count = hand_card.union_card_info[t][i]
        #                 if count == 0:
        #                     return False
        st = time.time()
        j, s, k = card_analyse.get_jiang_ke_shun(hand_card.hand_card_vals)
        print("took =", time.time()- st)
        if hand_card.chi_card_vals:
            s.extend(hand_card.chi_card_vals)
        if len(s) < 2:
            return False
        s.sort()
        print("s=", s)
        for i in range(len(s)):
            shun = s[i]
            for c in range(i + 1, len(s)):
                if shun[-1]+1 == s[c][0]:
                    return True
        return False


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
        1: [6, 0, 0, 0, 1, 1, 1, 1, 1, 1],  # 万
        2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
        3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
        4: [2, 2, 0, 0, 0],                 # 风
        5: [3, 3, 0, 0],                    # 箭
    }
    hand_card.chi_card_vals=[[23,24,25]]
    hand_card.handle_hand_card_for_settle_show()
    hand_card.union_hand_card()
    print("hand_card =", hand_card.hand_card_vals)
    test_type = LianLiu()
    start_time = time.time()
    print(test_type.is_this_type(hand_card, card_analyse))
    print("time = ", time.time() - start_time)