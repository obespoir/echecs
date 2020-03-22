# coding=utf-8

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.constants.carddefine import CardType

class ZiMo(BaseType):
    """
    9)	自摸：自己摸到牌成胡。
    """
    def __init__(self):
        super(ZiMo, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        return hand_card.zi_mo