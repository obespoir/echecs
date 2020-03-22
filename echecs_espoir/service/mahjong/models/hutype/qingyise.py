# coding=utf-8

from service.mahjong.models.hutype.basetype import BaseType


class QingYiSe(BaseType):
    """
    清一色
    """
    def __init__(self):
        super(QingYiSe, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        pass