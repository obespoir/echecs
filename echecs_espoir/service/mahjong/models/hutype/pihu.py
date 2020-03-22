# coding=utf-8

from service.mahjong.models.hutype.basetype import BaseType
from service.mahjong.models.utils.cardanalyse import CardAnalyse


class PiHu(BaseType):
    """
    屁胡
    """
    def __init__(self):
        super(PiHu, self).__init__()

    def is_this_type(self, hand_card, card_analyse=CardAnalyse()):
        ret = card_analyse.get_can_pi_hu_info_by_val(hand_card.hand_card_vals)
        return 1 if ret else 0

