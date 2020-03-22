# coding=utf-8

from service.mahjong.models.hutype.basetype import BaseType


class PengPengHu(BaseType):
    """
    碰碰胡
    """
    def __init__(self):
        super(PengPengHu, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        pass