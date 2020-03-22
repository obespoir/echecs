# coding=utf-8
import time

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType, CARD_SIZE
from service.mahjong.models.card.hand_card import HandCard
from service.mahjong.models.card.card import Card
from service.mahjong.models.utils.cardanalyse import CardAnalyse


class MiaoShouHuiChun(BaseType):
    """
    1)	妙手回春：自摸牌墙上最后一张牌胡牌。
    不记番： 自摸
    """

    def __init__(self):
        super(MiaoShouHuiChun, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        used_card_type = [CardType.WAN]  # 此游戏中使用的花色
        remain_card_count = hand_card.game_data.card_dealer.card_count
        is_zi_mo = hand_card.zi_mo
        return remain_card_count == 0 and is_zi_mo



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
    test_type = MiaoShouHuiChun()
    start_time = time.time()
    print(test_type.is_this_type(hand_card, card_analyse))
    print("time = ", time.time() - start_time)