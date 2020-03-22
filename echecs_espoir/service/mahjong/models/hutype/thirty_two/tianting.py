# coding=utf-8
import time

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType, CARD_SIZE
from service.mahjong.models.card.hand_card import HandCard
from service.mahjong.models.card.card import Card
from service.mahjong.models.utils.cardanalyse import CardAnalyse


class TianTing(BaseType):
    """
    4)	天听：庄家打出第一张牌时报听称为报听；发完牌后闲家便报听也称为天听。天听要在胡牌后才算番，如果发完牌后有补花，补花之后报听也算天听。如果庄家在发完牌后有暗杠，则庄家不算天听，
    计报听。
    """

    def __init__(self):
        super(TianTing, self).__init__()

    def is_this_type(self, hand_card, card_analyse):

        return bool(hand_card.is_tian_ting)



if __name__ == "__main__":
    pass
    card_analyse = CardAnalyse()
    hand_card = HandCard(0, None)
    hand_card.hand_card_info = {
        1: [9, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 万
        2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
        3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
        4: [2, 2, 0, 0, 0],                 # 风
        5: [3, 3, 0, 0],                    # 箭
    }
    # hand_card.hand_card_info = {
    #     1: [6, 3, 0, 0, 0, 0, 0, 0, 0, 3],  # 万
    #     2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
    #     3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
    #     4: [6, 3, 3, 0, 0],                 # 风
    #     5: [2, 2, 0, 0],                    # 箭
    #
    # }
    hand_card.handle_hand_card_for_settle_show()
    hand_card.union_hand_card()
    print("hand_card =", hand_card.hand_card_vals)
    test_type = TianTing()
    start_time = time.time()
    print(test_type.is_this_type(hand_card, card_analyse))
    print("time = ", time.time() - start_time)