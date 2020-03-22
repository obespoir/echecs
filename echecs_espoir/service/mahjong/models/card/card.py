# coding=utf-8

from service.mahjong.constants.carddefine import CARD_SIZE, CardType, CARD_DESC_TABLE


class Card(object):
    """
    麻将卡牌，八位二进制表示，前四位表示花色，后四位表示位数
    """
    def __init__(self, card_type, digit):
        self.card_type = card_type
        self.digit = digit
        self.card_val = Card.cal_card_val(card_type, digit)

    @staticmethod
    def cal_card_val(card_type, digit):
        return ((card_type << 4) & 0xF0) | (digit & 0x0F)

    @staticmethod
    def cal_card_type(card_val):
        return (card_val >> 4) & 0x0F

    @staticmethod
    def cal_card_digit(card_val):
        return card_val & 0x0F

    @staticmethod
    def get_next_card_val(card_val):
        card_type = Card.cal_card_type(card_val)
        digit = Card.cal_card_digit(card_val)
        digit += 1
        if digit >= CARD_SIZE[card_type]:
            digit = 1
        return Card.cal_card_val(card_type, digit)

    @staticmethod
    def create_card_by_val(card_val):
        return Card(Card.cal_card_type(card_val), Card.cal_card_digit(card_val))

    @staticmethod
    def has_shun(card_val):
        card_type = Card.cal_card_type(card_val)
        return card_type in [CardType.WAN, CardType.BING, CardType.TIAO]

    def is_num_card(self):
        return self.card_type in [CardType.WAN, CardType.BING, CardType.TIAO]

    def is_feng_card(self):
        return self.card_type == CardType.FENG

    def is_jian_card(self):
        return self.card_type == CardType.JIAN

    def is_hua_card(self):
        return self.card_type == CardType.HUA

    @property
    def next_card(self):
        digit = self.digit + 1
        if digit >= CARD_SIZE[self.card_type]:
            digit = 1
        return Card(self.card_type, digit)

    def __str__(self):
        return "<Card[%s]:%s>" % (self.card_val, CARD_DESC_TABLE[self.card_type][self.digit])