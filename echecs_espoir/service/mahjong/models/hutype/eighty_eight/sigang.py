# coding=utf-8

from service.mahjong.models.hutype.basetype import BaseType


class SiGang(BaseType):
    """
    4)	四杠: 胡牌时，牌里有4副杠，明暗杠均可
    不记番：三杠、双暗杠、双明杠、明杠、暗杠、单钓
    """
    def __init__(self):
        super(SiGang, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        gang_lst = []
        dian_gang_card_vals = hand_card.dian_gang_card_vals
        bu_gang_card_vals = hand_card.bu_gang_card_vals
        an_gang_card_vals = hand_card.an_gang_card_vals
        gang_lst.extend(dian_gang_card_vals)
        gang_lst.extend(bu_gang_card_vals)
        gang_lst.extend(an_gang_card_vals)
        return len(gang_lst) == 4