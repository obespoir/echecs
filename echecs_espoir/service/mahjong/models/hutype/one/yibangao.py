# coding=utf-8

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType

class YiBanGao(BaseType):
    """
    一般高
    """
    def __init__(self):
        super(YiBanGao, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        j, s, k = card_analyse.get_jiang_ke_shun(hand_card.hand_card_vals)
        if hand_card.chi_card_vals:
            for chi_group in hand_card.chi_card_vals:
                chi_group.sort()
                s.append(chi_group)

        while True:
            if not s:
                break
            shun_group = s.pop()
            if shun_group in s:
                return True

        return False