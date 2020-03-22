# coding=utf-8
import copy
from functools import reduce

from service.mahjong.constants.carddefine import CardType, CARD_SIZE, LAI_ZI
from service.mahjong.models.card.card import Card


class PiHuAnalyse(object):
    """
    基本屁胡(可有癞子)分析
    """
    def __init__(self, card_type_list=[CardType.WAN]):
        self.card_range = []
        for t in card_type_list:
            self.card_range.append([Card.cal_card_val(t, 1), Card.cal_card_val(t, CARD_SIZE[t]-1)])

    def ke(self, card_list):
        """
        判断列表中是否相同的牌
        :param card_list: 牌值列表
        """
        for i in range(1, len(card_list)):
            if card_list[i] != card_list[i - 1]:
                return False
        return True

    def shun(self, card_list):
        """
        判断列表中是否为顺子
        :param card_list: 列表，前三个元素值按大小升序排列
        """
        return card_list[0] == card_list[1] + 1 == card_list[2] + 2

    def _index_card(self, card_list, item):
        """
        检索某张牌是否在列表中
        :param ls: 牌值列表
        :param item: 待检索的牌
        """
        for i in range(len(card_list)):
            if card_list[i] == item:
                return i
        return -1

    def _drop(self, card_list, n):
        """
        从列表最后中取特定张牌
        :param card_list: 牌值列表
        :param n: 几张牌
        """
        rst = card_list[n:]
        return rst

    def _delete(self, card_list, items):
        """
        从列表中删除某些牌
        :param ls: 牌值列表
        :param items: 待删除的牌列表
        """
        rst = card_list[:]
        for i in items:
            rst.remove(i)
        return rst

    def hu(self, js, ls):
        """
        实际判胡
        :param js: 列表， 癞子列表
        :param ls: 列表， 普通牌列表
        :return: 返回[[顺子/刻子1], [顺子/刻子2], ...]
        """
        # global cut
        # cut += 1
        jlen = len(js)
        llen = len(ls)
        rst = [[] for _ in range(6)]
        if llen == 0:
            return [[js]]
        if jlen + llen == 3:
            if jlen >= 2 or \
                    (jlen == 1 and (self.ke(ls) or abs(ls[0] - ls[1]) <= 2)) or \
                    (jlen == 0 and (self.ke(ls) or self.shun(ls))):
                return [[js + ls]]
            else:
                return []
        elif jlen + llen > 3:
            s1, s2 = self._index_card(ls, ls[0] - 1), self._index_card(ls, ls[0] - 2)
            if llen >= 3 and self.ke(ls[:3]):
                rst[0] = list(map(lambda x: [ls[:3]] + x, self.hu(js, ls[3:])))
            if s1 != -1 and s2 != -1:
                tmp = [ls[0], ls[s1], ls[s2]]
                rst[1] = list(map(lambda x: [tmp] + x, self.hu(js, self._delete(ls, tmp))))
            if jlen > 0 and llen >= 2 and self.ke(ls[:2]):
                tmp = [js[0]] + ls[:2]
                rst[2] = list(map(lambda x: [tmp] + x, self.hu(js[1:], ls[2:])))
            if jlen > 0 and s1 != -1:
                tmp = [js[0], ls[0], ls[s1]]
                rst[3] = list(map(lambda x: [tmp] + x, self.hu(js[1:], self._delete(ls, [ls[0], ls[s1]]))))
            if jlen > 0 and s2 != -1:
                tmp = [js[0], ls[0], ls[s2]]
                rst[4] = list(map(lambda x: [tmp] + x, self.hu(js[1:], self._delete(ls, [ls[0], ls[s2]]))))
            if jlen > 1:
                tmp = [js[0], js[1], ls[0]]
                rst[5] = list(map(lambda x: [tmp] + x, self.hu(js[2:], ls[1:])))
            return reduce(lambda x, y: x + y, rst)

    def get_hu_detail(self, card_list):
        """
        胡牌判断
        :param card_list: 牌值列表
        :return: 返回所有胡牌详细信息[胡法1, 胡法2, ...]
                胡法1 = [[将牌], [[顺子/刻子1], [顺子/刻子2], ...]]]
        """
        temp_card_list = copy.deepcopy(card_list)
        rst = []
        for c in temp_card_list:
            if CardType.HUA == Card.cal_card_type(c):
                # 如果牌中有花,则不能为屁胡
                return rst

        num_len = len(card_list)
        if num_len % 3 == 2:
            card_list.sort(key=lambda x: -x)
            card_list = self.trans_non_num_card_to_gap(card_list)
            jiang = []
            tmpset = set()

            # 首先求出所有的将牌组合
            for i in range(num_len-1):
                for j in range(i + 1, num_len):
                    if card_list[i] == card_list[j] or card_list[i] + card_list[j] > LAI_ZI:
                        if card_list[i] * LAI_ZI + card_list[j] not in tmpset:
                            jiang.append([card_list[i], card_list[j]])
                            tmpset.add(card_list[i] * LAI_ZI + card_list[j])
            for it in jiang:
                tmp = self._delete(card_list, it)
                jp = [x for x in tmp if x >= LAI_ZI]
                lp = [x for x in tmp if x < LAI_ZI]
                # jp = filter(lambda x: x >= LAI_ZI, tmp)
                # lp = filter(lambda x: x < LAI_ZI, tmp)
                rst += list(map(lambda x: [it, x], self.hu(jp, lp)))
            rst = self.trans_non_num_card_from_gap_plus(rst)
        return rst

    def trans_non_num_card_to_gap(self, card_list):
        """
        将非数字牌（风,箭,字,花）值转换成 间断的，避免误判为顺子
        :param card_list:
        :return:
        """
        result = []
        for c in card_list:
            if c == LAI_ZI:
                result.append(c)
                continue
            t = Card.cal_card_type(c)
            if CardType.HUA == t:
                continue
            if t in [CardType.FENG, CardType.JIAN]:
                result.append(Card.cal_card_val(t, Card.cal_card_digit(c)*3))
            else:
                result.append(c)
        return result

    def trans_non_num_card_from_gap(self, card_list):
        """
        将间断的非数字牌（风,箭,字,花）值转换成原始值
        :param card_list:
        :return:
        """
        ret = [[] for _ in range(len(card_list))]
        for f, cards in enumerate(card_list):
            jiang = copy.deepcopy(cards[0])
            other_card = copy.deepcopy(cards[1])

            jiang_vals = jiang[0] if jiang[0] == jiang[1] else jiang[0] + jiang[1] - LAI_ZI
            jiang_type = Card.cal_card_type(jiang_vals)
            jiang_lst = []
            for index, j in enumerate(jiang):
                if jiang_type in [CardType.FENG, CardType.JIAN] and jiang[index]!=LAI_ZI:
                    jiang_lst.append(Card.cal_card_val(jiang_type, Card.cal_card_digit(jiang[index])//3))
                else:
                    jiang_lst.append(j)
            ret[f].append(jiang_lst)

            shun_ke_lst= []
            for shun_ke in other_card:
                tmp_shun_ke = copy.deepcopy(shun_ke)
                for index, i in enumerate(tmp_shun_ke):
                    if i == LAI_ZI:
                        continue
                    t = Card.cal_card_type(i)
                    if t in [CardType.FENG, CardType.JIAN]:
                        tmp_shun_ke[index] = Card.cal_card_val(t, Card.cal_card_digit(i) // 3)
                shun_ke_lst.append(tmp_shun_ke)
            ret[f].append(shun_ke_lst)

        return ret


    def trans_non_num_card_from_gap_plus(self, card_list):
        """
        将间断的非数字牌（风,箭,字,花）值转换成原始值
        :param card_list:
        :return:
        """
        ret = [[] for _ in range(len(card_list))]  # 最终输出结果集
        for f, cards in enumerate(card_list):
            jiang = cards[0]
            other_card = cards[1]
            ret_jiang = []              # 结果的将牌
            ret_other_card = []         # 结果的顺和刻

            for j in jiang:
                jiang_type = Card.cal_card_type(j)
                if jiang_type in [CardType.FENG, CardType.JIAN]:
                    ret_jiang.append(Card.cal_card_val(jiang_type, Card.cal_card_digit(j) // 3))
                else:
                    ret_jiang.append(j)
            ret[f].append(ret_jiang)

            for shun_ke in other_card:
                sk_lst = []
                for i in shun_ke:
                    sk_type = Card.cal_card_type(i)
                    if sk_type in [CardType.FENG, CardType.JIAN]:
                        sk_lst.append(Card.cal_card_val(sk_type, Card.cal_card_digit(i) // 3))
                    else:
                        sk_lst.append(i)
                ret_other_card.append(sk_lst)
            ret[f].append(ret_other_card)

        return ret


    def get_shun_liang_tou_card(self, card_1, card_2):
        """
        获取顺子两头的牌, card_1=card_2+1
        """
        if card_1 != card_2+1:
            return []

        ret = []
        for r in self.card_range:
            if card_1+1 <= r[1] and card_1+1>=r[0]:
                ret.append(card_1+1)
                break
        for r in self.card_range:
            if card_2 - 1 <= r[1] and card_2 - 1 >= r[0]:
                ret.append(card_2 - 1)
                break
        return ret


    def get_lai_zi_card(self, hu_detail):
        """
        从胡牌中获取用癞子替代的牌
        :param hu_detail: 返回所有胡牌详细信息[胡法1, 胡法2, ...]
                胡法1 = [[将牌], [[顺子/刻子1], [顺子/刻子2], ...]]]
        :return:
        """
        ting_cards = []
        for card_list in hu_detail:
            jiang_cards = card_list[0]

            if LAI_ZI < jiang_cards[0] + jiang_cards[1]:
                 ting_cards.append(jiang_cards[0] + jiang_cards[1] - LAI_ZI)
            for cards in card_list[1]:
                if 3 == len(cards) and LAI_ZI == cards[0]:
                    if cards[1] == cards[2]+1:
                        ting_cards.extend(self.get_shun_liang_tou_card(cards[1], cards[2]))
                    elif cards[1] == cards[2]+2:
                        ting_cards.append(cards[1]-1)
                    elif cards[1]==cards[2]:
                        # 此组合为刻子
                        ting_cards.append(cards[1])
        return list(set(ting_cards))

    def get_ting_cards(self, card_list):
        """

        :param card_list:
        :return: []
        """
        return self.get_lai_zi_card(self.get_hu_detail(card_list))

if __name__ == '__main__':
    import time
    print('11111111111111111111111111111111111111111111111111111111111')
    import cProfile, pstats

    card_analyse = PiHuAnalyse(card_type_list=[CardType.WAN, CardType.BING, CardType.TIAO])
    # r = card_analyse.get_ting_cards([18, 18, 18, 19, 19, 19, 20, 20, 20, 23, 24, 25, 82, 10000])
    # print r
    r = card_analyse.get_hu_detail([18, 18, 18, 19, 19, 19, 20, 20, 20, 23, 24, 25, 82, 10000])
    print("r3=", r)
    r4 = card_analyse.get_lai_zi_card(r)
    print("r4=", r4)

    # r2 = card_analyse.get_hu_detail([17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 23])
    st = time.time()
    r2 = card_analyse.get_hu_detail([ 19, 19, 19, 20, 20, 21, 21, 22, 22, 23, 23])
    print("r2=",r2)
    print("time=", time.time() - st)
    '''
    #tt = profile.runcall("huex([LAI_ZI, 43, 43, 42, 42, 41, 41, 26, 26, 5, 4, 3, 3, 3])", "timeit")

    #pro = cProfile.Profile()
    #tt = pro.runcall(huex, [LAI_ZI, 43, 43, 42, 42, 41, 41, 26, 26, 5, 4, 3, 3, 3], "timeit")
    #print 'cProfile', tt

    p = pstats.Stats('timeit')
    p.sort_stats('time')
    p.print_stats(10)
    '''

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

    # t = time.time()
    # tmp = None
    # for i in range(LAI_ZI):
    #     # tmp = get_hu_detail([LAI_ZI, LAI_ZI, 81, 81, 47, 46, 26, 25, 7, 6, 5, 4, 4, 4])
    #     tmp = card_analyse.get_hu_detail([LAI_ZI, 6, 47, 47, 29, 29, 29, 25, 24, 23, 7, 7, 5, 5])
    #     # print "tmp=", tmp
    # print tmp
    # print '%.6f' % ((time.time() - t) / 1000.0)
    # print "ting_cards=", card_analyse.get_lai_zi_card(tmp)

    # print cut / LAI_ZI
    # print card_analyse.get_can_chi_info(52, [49,50,51,52,53,54])

