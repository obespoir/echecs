# coding=utf-8

from service.mahjong.models.hutype.basetype import BaseType


class MingGang(BaseType):
    """
    一般高
    """
    def __init__(self):
        super(MingGang, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        if hand_card.dian_gang_card_vals:
            return True
        if hand_card.bu_gang_card_vals:
            return True
