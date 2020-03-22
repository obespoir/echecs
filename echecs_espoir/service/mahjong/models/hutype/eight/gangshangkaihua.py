# coding=utf-8
import time

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType, CARD_SIZE
from service.mahjong.models.card.hand_card import HandCard
from service.mahjong.constants.gamedefine import Act
from service.mahjong.models.utils.cardanalyse import CardAnalyse


class GangShangKaiHua(BaseType):
    """
    3)	杠上开花：胡牌时，开杠抓进的牌成胡牌（不包括补花）。
    不记番：自摸
    """

    def __init__(self):
        super(GangShangKaiHua, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        if len(hand_card.game_data.act_record_list)< 1:
            return False
        record = hand_card.game_data.act_record_list[-1]
        # 倒数第一个动作为杠　
        return record.act_type in [Act.BU_GANG, Act.DIAN_GANG, Act.AN_GANG]



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
    test_type = GangShangKaiHua()
    start_time = time.time()
    print(test_type.is_this_type(hand_card, card_analyse))
    print("time = ", time.time() - start_time)