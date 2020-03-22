# coding=utf-8

from service.mahjong.models.hutype.basetype import BaseType


class ShiSanYao(BaseType):
    """
    十三幺
    """
    def __init__(self):
        super(ShiSanYao, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        ret = card_analyse.get_can_shi_san_yao_by_val(hand_card.hand_card_vals)
        return 1 if ret else 0
