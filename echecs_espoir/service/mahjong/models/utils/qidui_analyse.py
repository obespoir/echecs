# coding=utf-8
import copy

from service.mahjong.constants.carddefine import CardType, CARD_SIZE, LAI_ZI
from service.mahjong.models.card.card import Card


class QiDuiAnalyse(object):
    """
    七对(可有癞子)分析
    """
    def __init__(self, card_type_list=[CardType.WAN]):
        self.card_range = []
        for t in card_type_list:
            self.card_range.append([Card.cal_card_val(t, 1), Card.cal_card_val(t, CARD_SIZE[t])])

    def get_hu_detail(self, card_list):
        """
        七对判断
        :param card_list: 牌值列表
        :return: 返回所有胡牌信息[[对子１], [对子２], ...]]]
        """
        temp_card_list = copy.deepcopy(card_list)
        if 14 == len(temp_card_list):
            lai_zi_num = sum(temp_card_list)/LAI_ZI

            temp = [temp_card_list[0]]
            for i in range(1, 14):
                if LAI_ZI != temp_card_list[i] and temp_card_list[i] == temp[i-1]:
                    temp.append(0)
                else:
                    temp.append(temp_card_list[i])
            dui_num = 0
            for j in temp:
                if 0 == j:
                    dui_num += 1
            if 7 <= dui_num + lai_zi_num:
                hu_info = []
                for k in range(1, 14):
                    if 0 == temp[k]:
                        hu_info.append([temp[k-1], temp[k-1]])
                    elif 0 != temp[k-1] and LAI_ZI != temp[k-1]:
                        hu_info.append([temp[k-1], LAI_ZI])
                for _ in range(7-len(hu_info)):
                    print("aaaaaaaaaaaaaaaaaa:", len(hu_info))
                    hu_info.append([LAI_ZI, LAI_ZI])
                return hu_info
        return []

    def get_lai_zi_card(self, card_list):
        """
        从胡牌中获取用癞子替代的牌
        :param card_list: [[对子１], [对子２], ...]]]
        :return:
        """
        ting_cards = []
        lai_zi_dui = 0
        dui_cards = []
        for dui_zi in card_list:
            if LAI_ZI == dui_zi[1]:
                if dui_zi[0] != dui_zi[1]:
                    ting_cards.append(dui_zi[0])
                else:
                    lai_zi_dui += 1
            else:
                dui_cards.append(dui_zi[0])
        if lai_zi_dui:
            ting_cards.extend(dui_cards)

        return list(set(ting_cards))

    def get_ting_cards(self, card_list):
        return self.get_lai_zi_card(self.get_hu_detail(card_list))

if __name__ == '__main__':
    print('11111111111111111111111111111111111111111111111111111111111')
    import cProfile, pstats

    card_analyse = QiDuiAnalyse(card_type_list=[CardType.WAN, CardType.BING, CardType.TIAO])

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
        tmp = card_analyse.get_hu_detail([18, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, LAI_ZI, LAI_ZI, LAI_ZI])
        # print "tmp=", tmp
    print("hu_detail:", tmp)
    print('%.6f' % ((time.time() - t) / 1000.0))
    print("ting_card=", card_analyse.get_lai_zi_card(tmp))

    # print cut / LAI_ZI
    # print card_analyse.get_can_chi_info(52, [49,50,51,52,53,54])

