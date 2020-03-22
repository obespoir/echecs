# coding=utf-8

from service.mahjong.models.hutype.basetype import BaseType


class QiXiaoDui(BaseType):
    """
    1)	七对: 胡牌时，牌型由7个对子组成。
    不记番：门前清、单钓将、自摸（可算不求人） 。
    """
    def __init__(self):
        super(QiXiaoDui, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        ret = card_analyse.get_can_qi_dui_by_val(hand_card.hand_card_vals)
        return 1 if ret else 0