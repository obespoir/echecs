# coding=utf-8
import copy

from service.mahjong.constants.carddefine import CardType, CARD_SIZE, LAI_ZI
from service.mahjong.models.card.card import Card

SHI_SAN_YAO = [17, 25, 33, 41, 49, 57, 65, 66, 67, 68, 81, 82, 83]


class ShiSanYaoAnalyse(object):
    """
    十三幺(可有癞子)分析
    """
    def __init__(self, card_type_list=[CardType.WAN]):
        self.card_range = []
        for t in card_type_list:
            self.card_range.append([Card.cal_card_val(t, 1), Card.cal_card_val(t, CARD_SIZE[t])])

    def get_hu_detail(self, card_list):
        """
        七对判断
        :param card_list: 牌值列表[card1, ..., laizi1, ...]
        :return: 返回所有胡牌信息[card1, ..., laizi1, ...]
        """
        temp_card_list = copy.deepcopy(card_list)
        if 14 == len(temp_card_list):
            lai_zi_num = sum(temp_card_list) / LAI_ZI
            temp = list(set(SHI_SAN_YAO) - set(temp_card_list))
            if lai_zi_num >= len(temp):
                return temp_card_list
        return []

    def get_lai_zi_card(self, card_list):
        """
        从胡牌中获取用癞子替代的牌
        :param card_list: [card1, ..., laizi1, ...]
        :return:
        """
        ting_cards = []
        temp = list(set(SHI_SAN_YAO) - set(card_list))
        lai_zi_num = sum(card_list) / LAI_ZI
        if temp and 1 == lai_zi_num:
            ting_cards.extend(temp)
        else:
            ting_cards.extend(SHI_SAN_YAO)
        return ting_cards

    def get_ting_cards(self, card_list):
        return self.get_lai_zi_card(self.get_hu_detail(card_list))

if __name__ == '__main__':
    import cProfile, pstats

    card_analyse = ShiSanYaoAnalyse(card_type_list=[CardType.WAN, CardType.BING, CardType.TIAO])

    import time

    # t = time.time()
    # for i in range(LAI_ZI):
    #     tmp = huex([LAI_ZI, LAI_ZI, 47, 47, 29, 29, 29, 25, 24, 23, 7, 7, 5, 5])
    # print '%.6f' % ((time.time() - t) / LAI_ZI.0)
    # for x in tmp:
    #     print x
    #
    # t = time.time()
    # for i in range(LAI_ZI):
    #     tmp = huex([LAI_ZI, 43, 43, 42, 42, 41, 41, 26, 26, 5, 4, 3, 3, 3])
    # print '%.6f' % ((time.time() - t) / LAI_ZI.0)
    # for x in tmp:
    #     print x

    t = time.time()
    tmp = None
    for i in range(1000):
        # tmp = get_hu_detail([LAI_ZI, LAI_ZI, 81, 81, 47, 46, 26, 25, 7, 6, 5, 4, 4, 4])
        # tmp = card_analyse.get_hu_detail([LAI_ZI, 6, 47, 47, 29, 29, 29, 25, 24, 23, 7, 7, 5, 5])
        tmp = card_analyse.get_hu_detail([17, 25, 33, 41, 49, 57, 65, 66, 67, 68, 81, 82, LAI_ZI, LAI_ZI])
        # print "tmp=", tmp
    print("hu_detail:", tmp)
    print('%.6f' % ((time.time() - t) / 1000.0))
    print("ting_card=", card_analyse.get_lai_zi_card(tmp))

    # print cut / LAI_ZI
    # print card_analyse.get_can_chi_info(52, [49,50,51,52,53,54])

