# coding=utf-8


class ChiCardInfo(object):
    """
    吃牌信息
    """
    def __init__(self, chi_card_val, chi_card_val_lst, seat_id):
        self.chi_card_val = chi_card_val       # 被吃的牌
        self.seat_id = seat_id
        self.chi_card_val_lst = []         # 吃的全部三张牌，一般被吃的牌放第一张
        map(lambda card_val: self.chi_card_val_lst.append(card_val), chi_card_val_lst)
