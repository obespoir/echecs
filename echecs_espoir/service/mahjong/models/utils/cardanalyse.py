# coding=utf-8

import copy
import time

from service.mahjong.constants.carddefine import CardType, LAI_ZI, HuType
from service.mahjong.models.card.card import Card
from service.mahjong.models.utils.pihu_analyse import PiHuAnalyse
from service.mahjong.models.utils.qidui_analyse import QiDuiAnalyse
from service.mahjong.models.utils.shisanyao_analyse import ShiSanYaoAnalyse


class CardAnalyse(object):
    """
    牌值分析，吃，碰，杠，基本屁胡
    """
    def __init__(self, card_type_list=[CardType.WAN], base_hu_type=[HuType.PI_HU, HuType.QI_XIAO_DUI, HuType.SHI_SAN_YAO]):
        self.hu_analyse = PiHuAnalyse(card_type_list=card_type_list)
        self.qidui_analyse = QiDuiAnalyse(card_type_list=card_type_list) if HuType.QI_XIAO_DUI in base_hu_type else None
        self.shisanyao_analyse = ShiSanYaoAnalyse(card_type_list) if HuType.SHI_SAN_YAO in base_hu_type else None

    def shun(self, card_list):
        """
        判断列表中是否为顺子
        :param card_list: 列表，前三个元素值按大小升序排列
        """
        return card_list[2] == card_list[1] + 1 == card_list[0] + 2

    def get_can_chi_info_by_val(self, card, cur_card_list):
        """
        判断某张牌是否可以吃
        :param card: 待判断的牌
        :param cur_card_list: 当前手牌
        :return: 返回吃牌的组合[[], [], ...]
        """
        if not Card.has_shun(card):
            return []
        tmp = []
        for i in range(card+2, card-3, -1):
            if i in tmp:
                continue
            if i == card:
                tmp.append(i)
            else:
                if i in cur_card_list:
                    tmp.append(i)

        result = []
        num = len(tmp)
        if 3 > num:
            return []
        for j in range(num-2):
            if self.hu_analyse.shun(tmp[j:j+3]):
                result.append(tmp[j:j+3])
        return result

    def get_can_chi_info_by_handcard(self, card, hand_card):
        """
        判断某张牌是否可以吃
        :param card: 待判断的牌
        :param hand_card: 当前手牌
        :return: 返回吃牌的组合[[], [], ...]
        """
        return self.get_can_chi_info_by_val(card, hand_card.hand_card_vals)

    def get_can_peng_info_by_val(self, card, cur_card_list):
        """
        判断某张牌是否可以碰
        :param card: 待判断的牌
        :param cur_card_list: 当前手牌
        :return: 返回是否可碰牌
        """
        return 2 <= cur_card_list.count(card)

    def get_can_peng_info_by_handcard(self, card, hand_card):
        """
        判断某张牌是否可以碰
        :param card: 待判断的牌
        :param cur_card_list: 当前手牌
        :return: 返回是否可碰牌
        """
        card_type = Card.cal_card_type(card)
        card_digit = Card.cal_card_digit(card)
        return 2 <= hand_card.hand_card_info[card_type][card_digit]

    def get_can_dian_gang_info_by_handcard(self, card, hand_card):
        """
        判断某张牌是否可以杠（点杠）
        :param card: 待判断的牌
        :param cur_card_list: 当前手牌
        :return: 返回是否可杠牌
        """
        card_type = Card.cal_card_type(card)
        card_digit = Card.cal_card_digit(card)
        return 4 == hand_card.hand_card_info[card_type][card_digit]

    def get_can_gang_info_by_handcard(self, card, hand_card):
        """
        判断某张牌是否可以杠（点杠/补杠）
        :param card: 待判断的牌
        :param cur_card_list: 当前手牌
        :return: 返回是否可杠牌
        """
        card_type = Card.cal_card_type(card)
        card_digit = Card.cal_card_digit(card)
        return 4 == hand_card.peng_card_vals.count(card)+hand_card.hand_card_info[card_type][card_digit]

    def get_can_an_gang_info_by_handcard(self, card, hand_card):
        """
        判断某张牌是否可以暗杠
        :param card: 待判断的牌
        :param cur_card_list: 当前手牌
        :return: 返回是否可暗杠牌
        """
        card_type = Card.cal_card_type(card)
        card_digit = Card.cal_card_digit(card)
        return 4 == hand_card.hand_card_info[card_type][card_digit]

    def get_can_pi_hu_info_by_val(self, card_list):
        """
         屁胡类型判断
        :param card_list: 牌值列表 2 == len(card_list) % 3
        :return: 返回所有胡牌详细信息[胡法1, 胡法2, ...]
                胡法1 = [[将牌], [[顺子/刻子1], [顺子/刻子2], ...]]]
        """
        return self.hu_analyse.get_hu_detail(card_list)

    def get_can_qi_dui_by_val(self, card_list):
        """
        七对类型判断
        :param card_list: 14 == len(card_list), list为有序列表, 包括癞子
        :return: card_list
        """
        if self.qidui_analyse:
            return self.qidui_analyse.get_hu_detail(card_list)
        return []

    def get_can_shi_san_yao_by_val(self, card_list):
        """
        判断是否十三幺
        :param card_list: 14 == len(card_list), list为有序列表, 包括癞子
        :return:
        """
        if self.shisanyao_analyse:
            return self.shisanyao_analyse.get_hu_detail(card_list)
        return []

    def get_hu_by_val(self, card_list):
        """
        获取是否可以胡基本牌型
        :param card_list: 牌值列表 2 == len(card_list) % 3
        :return: {基本牌型：[胡法列表], ...}
        """
        ret = {}
        pi_hu = self.get_can_pi_hu_info_by_val(card_list)

        qi_xiao_dui = self.get_can_qi_dui_by_val(card_list)
        shi_san_yao = self.get_can_shi_san_yao_by_val(card_list)
        if pi_hu:
            ret[HuType.PI_HU] = pi_hu
        if qi_xiao_dui:
            print("qi_xiao_dui=",qi_xiao_dui)
            ret[HuType.QI_XIAO_DUI] = qi_xiao_dui
        if shi_san_yao:
            ret[HuType.SHI_SAN_YAO] = shi_san_yao

        return ret

    def get_can_ting_info_by_val(self, card_list):
        """
        听牌判断
        :param card_list: 牌值列表, 一般为13张牌＋癞子
        :return: 返回所有听牌{HuType: [ting_cards], ...}
        """
        ting_cards = {}
        temp_card_vals = copy.deepcopy(card_list)
        pi_hu_ting = self.hu_analyse.get_ting_cards(temp_card_vals)
        if pi_hu_ting:
            ting_cards[HuType.PI_HU] = pi_hu_ting
        temp_card_vals = copy.deepcopy(card_list)
        if self.qidui_analyse:
            ret = self.qidui_analyse.get_ting_cards(temp_card_vals)
            if ret:
                ting_cards[HuType.QI_XIAO_DUI] = ret
        temp_card_vals = copy.deepcopy(card_list)
        if self.shisanyao_analyse:
            ting_cards[HuType.SHI_SAN_YAO] = self.shisanyao_analyse.get_ting_cards(temp_card_vals)
        return ting_cards

    def get_jiang_ke_shun(self, card_list):
        """
        获取当前胡牌时候  的将顺刻
        :param hand_card:
        :param card_analyse:
        :return: jiang_card_group = [[17,17]]
        :return: shun_card_group=[[17, 18, 19], [17, 18, 19]]
        :return: ke_card_group=[[66, 66, 66], [24, 24, 24]]
        """
        jiang_card_group = []
        shun_card_group = []
        ke_card_group = []
        hu_type_group = self.get_can_pi_hu_info_by_val(card_list)
        # print "hu_type_group=", hu_type_group
        if not hu_type_group:
            return [], [], []
        jiang_card_group.append(hu_type_group[0][0])
        for lst in hu_type_group[0][1]:
            if self.hu_analyse.ke(lst):
                ke_card_group.append(lst)
            else:
                lst.sort()
                shun_card_group.append(lst)
        return jiang_card_group, shun_card_group, ke_card_group

    def get_jiang_ke_shun_plus(self, card_list):
        """
        获取当前胡牌时候  的将顺刻 升级版
        :param hand_card:
        :param card_analyse:
        :return: ret =[ [[[17,17]],[[17, 18, 19], [17, 18, 19]],[[66, 66, 66], [24, 24, 24]]], ...]
        """
        ret = []

        hu_type_group = self.get_can_pi_hu_info_by_val(card_list)
        # print "hu_type_group=", hu_type_group
        if not hu_type_group:
            return []
        for jsk_group in hu_type_group:
            data = {"j":[], "s":[], "k":[]}
            data["j"].append(jsk_group[0])
            for lst in jsk_group[1]:
                if self.hu_analyse.ke(lst):
                    data["k"].append(lst)
                else:
                    lst.sort()
                    data["s"].append(lst)
            ret.append(data)
        return ret


if __name__ == '__main__':
    import cProfile, pstats

    card_analyse = CardAnalyse(card_type_list=[CardType.WAN, CardType.BING, CardType.TIAO],base_hu_type=[HuType.PI_HU, HuType.QI_XIAO_DUI])

    r1 = card_analyse.get_can_qi_dui_by_val([17, 18, 18, 19, 19, 20, 20, 23, 23, 65, 65, 83, 83, 10000])
    print("7dui=", r1)
    r2 = card_analyse.get_hu_by_val([17, 17, 17, 18, 19, 20, 21, 22, 23, 24, 25, 25, 25, 10000])
    print("r2=", r2)


    temp_card_vals = [18, 18, 82, 19, 19, 19, 20, 20, 20, 23, 24, 25, 82, 10000]
    ting_infos = card_analyse.get_can_ting_info_by_val(temp_card_vals)
    print("ting_infos=", ting_infos)
    start = time.time()
    print("start=",start)
    for c in [17, 18, 19, 20, 21, 22, 23, 24, 25]:
        cards = copy.deepcopy(temp_card_vals)
        cards.append(LAI_ZI)
        cards.remove(c)
        ting_infos = card_analyse.get_can_ting_info_by_val(cards)
        print("check_ting_result ting_info=", ting_infos)

    print("耗时=", time.time() - start)
    '''
    #tt = profile.runcall("huex([LAI_ZI, 43, 43, 42, 42, 41, 41, 26, 26, 5, 4, 3, 3, 3])", "timeit")

    #pro = cProfile.Profile()
    #tt = pro.runcall(huex, [LAI_ZI, 43, 43, 42, 42, 41, 41, 26, 26, 5, 4, 3, 3, 3], "timeit")
    #print 'cProfile', tt

    p = pstats.Stats('timeit')
    p.sort_stats('time')
    p.print_stats(10)
    '''

    j, s, k = card_analyse.get_jiang_ke_shun([17, 17, 18, 18, 19, 19, 24, 24, 24, 25, 25, 66, 66, 66])
    print(j)
    print(s)
    print(k)

    import time


