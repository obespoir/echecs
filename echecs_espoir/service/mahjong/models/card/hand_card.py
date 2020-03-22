# coding=utf-8

import copy
from service.mahjong.constants.carddefine import CardType, CARD_SIZE, BLACK
from service.mahjong.models.card.card import Card


class HandCard(object):
    """
    手牌类不关注任何游戏逻辑，只负责存储部分数据,定义数据格式
    """
    def __init__(self, seat_id, game_data):
        self.game_data = game_data
        self.seat_id = seat_id
        self.hand_card_info = {}        # 手牌信息（不包括吃碰的牌）
        self.union_card_info = {}       # 全部手牌信息（包括吃碰）
        self.init_card_info()

        self.out_card_vals = []         # 已出的牌
        self.chi_card_vals = []         # 吃的牌
        self.peng_card_vals = []        # 碰的牌
        self.dian_gang_card_vals = []   # 点杠的牌
        self.bu_gang_card_vals = []     # 补杠的牌
        self.an_gang_card_vals = []     # 暗杠的牌
        self.ting_info_records = []     # 听牌信息记录
        self.i_can_see_cards = []       # 所有我可以见到的牌

        self.hua_card_vals = []         # 花牌
        self.last_card_val = BLACK      # 最后一张牌
        self.jiang_card_val = BLACK     # 将牌
        self.lou_hu_card_vals = []      # 当圈漏胡的牌

        self.dian_gang_source = {}     # 点杠的来源， {card_val: seat_id}
        self.shun_zi_info = None
        self.ke_zi_info = None
        self.hu_source_seat_id = -1   # 胡牌来源位置
        self.hand_card_for_settle_show = [[],[]]  # 记录吃碰杠顺序 用于结束游戏显示[[][][][手牌][胡牌]]
        self.guo_hu_num = 0      # 过胡次数
        self.bu_hua_num = 0      # 补花次数
        self.is_ting = 0            # 是否处于听牌状态
        self.is_tian_ting = 0       # 是否 天听, 用于牌型判定
        self.is_ren_hu = 0          # 是否 人胡, 用于牌型判定
        self.is_tian_hu = 0         # 是否 天胡, 用于牌型判定
        self.is_di_hu = 0           # 是否 地胡, 用于牌型判定
        self.hu_card_val = 0        # 胡的牌
        self.zi_mo = 0              # 1:表示自摸, 0:反之
        self.is_qiang_gang = 0      # 1:表示抢杠, 0:反之
        self.qiang_gang_hu_seat_id = -1    # 1:表示抢杠胡作为ID, -1:表示没有
        self.drewed_card_lst = []       # 从开局到最后所有摸过的牌



    def init_card_info(self):
        all_types = CardType.all_type()
        for t in all_types:
            self.hand_card_info[t] = [0 for _ in range(CARD_SIZE[t])]  # 列表第一个元素表示当种花色牌总数
            self.union_card_info[t] = [0 for _ in range(CARD_SIZE[t])]

    def reset_hand_card(self):
        self.hand_card_info = {}  # 手牌信息（不包括吃碰的牌）
        self.union_card_info = {}  # 全部手牌信息（包括吃碰）
        self.init_card_info()

        self.out_card_vals = []  # 已出的牌
        self.chi_card_vals = []  # 吃的牌
        self.peng_card_vals = []  # 碰的牌
        self.dian_gang_card_vals = []  # 点杠的牌
        self.bu_gang_card_vals = []  # 补杠的牌
        self.an_gang_card_vals = []  # 暗杠的牌
        self.ting_info_records = []  # 听牌信息记录
        self.i_can_see_cards = []  # 所有我可以见到的牌

        self.hua_card_vals = []  # 花牌
        self.last_card_val = BLACK  # 最后一张牌
        self.jiang_card_val = BLACK  # 将牌
        self.lou_hu_card_vals = []  # 当圈漏胡的牌

        self.dian_gang_source = {}  # 点杠的来源， {card_val: seat_id}
        self.shun_zi_info = None
        self.ke_zi_info = None
        self.hu_source_seat_id = -1  # 胡牌来源位置
        self.hand_card_for_settle_show = [[], []]  # 记录吃碰杠顺序 用于结束游戏显示[[][][][手牌][胡牌]]
        self.guo_hu_num = 0  # 过胡次数
        self.bu_hua_num = 0  # 补花次数
        self.is_ting = 0  # 是否处于听牌状态
        self.is_tian_ting = 0  # 是否 天听, 用于牌型判定
        self.is_ren_hu = 0  # 是否 人胡, 用于牌型判定
        self.is_tian_hu = 0  # 是否 天胡, 用于牌型判定
        self.is_di_hu = 0  # 是否 地胡, 用于牌型判定
        self.hu_card_val = 0  # 胡的牌
        self.zi_mo = 0  # 1:表示自摸, 0:反之
        self.is_qiang_gang = 0  # 1:表示抢杠, 0:反之
        self.qiang_gang_hu_seat_id = -1  # 1:表示抢杠胡作为ID, -1:表示没有
        self.drewed_card_lst = []  # 从开局到最后所有摸过的牌


    @property
    def hand_card_vals(self):
        ret = []
        for k, v in self.hand_card_info.items():
            if v[0] == 0:
                continue
            for i in range(1, CARD_SIZE[k]):
                if v[i] == 0:
                    continue
                for j in range(0, v[i]):
                    ret.append(Card.cal_card_val(k, i))
        return ret

    @property
    def get_an_gang_vals(self):
        return self.an_gang_card_vals
        pass

    def to_dict(self, is_own):
        """
        玩家当局牌信息
        :param is_own:　是否是玩家自己
        :return:
        """
        return {
            "seat_id": self.seat_id,
            "hand_card": self._hide_card(self.hand_card_vals, is_own),       # 当前手牌
            "out_card": self.out_card_vals,                     # 已出的牌
            "chi_card": self.chi_card_vals,                     # 吃的牌
            "peng_card": self.peng_card_vals,                   # 碰的牌
            "dian_gang_card": self.dian_gang_card_vals,         # 点杠的牌
            "bu_gang_card": self.bu_gang_card_vals,             # 补杠的牌
            "an_gang_card": self._hide_card(self.an_gang_card_vals, is_own),             # 暗杠的牌
            "hua_card": self.hua_card_vals,                     # 花牌
            "last_card": self.last_card_val,                    # 最后一张牌
            "dian_gang_source": self.dian_gang_source,          # 点杠的来源， {card_val: seat_id}
            "guo_hu_num": self.guo_hu_num,                      # 过胡次数， int
            "bu_hua_num": self.bu_hua_num,                      # 补花次数， int
            "hand_card_by_order": self.hand_card_for_settle_show  # 记录吃碰杠顺序
        }

    def to_dict_for_reconnect(self, is_own, is_god_perspective=0):
        """
        玩家当局牌信息
        :param is_own:　是否是玩家自己
        :param is_god_perspective:　是否是上帝视角
        :return:
        """
        self.handle_hand_card_for_settle_show()
        if is_god_perspective:
            hand_card_by_order = self.hand_card_for_settle_show
        else:
            hand_card_by_order = self._hide_card_by_order(self.hand_card_for_settle_show, is_own)
        return {
            "seat_id": self.seat_id,
            "hand_card": self._hide_card(self.hand_card_vals, is_own),       # 当前手牌
            "an_gang_card": self._hide_card(self.an_gang_card_vals, is_own),  # 暗杠的牌
            "out_card": self.out_card_vals,                     # 已出的牌
            "hua_card": self.hua_card_vals,                     # 花牌
            "last_card": self.last_card_val,                    # 最后一张牌
            "guo_hu_num": self.guo_hu_num,                      # 过胡次数， int
            "bu_hua_num": self.bu_hua_num,                      # 补花次数， int
            "is_ting": self.is_ting,                            # 是否听牌， int
            "hand_card_by_order": hand_card_by_order  # 记录吃碰杠顺序
        }

    def _hide_card(self, card_vals, is_own):
        if is_own:
            return card_vals
        num = len(card_vals)
        for i in range(num):
            if isinstance(i, list):
                for j in range(i):
                    card_vals[i][j] = BLACK
            else:
                card_vals[i] = BLACK
        return []

    def _hide_card_by_order(self, hand_card_for_settle_show, is_own):
        if is_own:
            return hand_card_for_settle_show
        tmp_hand_card = hand_card_for_settle_show[-2]
        for i in range(len(tmp_hand_card)):
            tmp_hand_card[i] = BLACK
        hand_card_for_settle_show[-2] = tmp_hand_card
        return hand_card_for_settle_show

    def has_card(self, card_val):
        """
        是否有指定的手牌
        :param card_val:
        :return: 返回张数
        """
        return self.hand_card_info[Card.cal_card_type(card_val)][Card.cal_card_digit(card_val)]

    def record_chi_card(self, chi_card_val, used_cards):
        self.chi_card_vals.append([chi_card_val, used_cards[0], used_cards[1]])
        # 记录吃碰杠顺序 用于结束游戏显示
        ret = [chi_card_val, used_cards[0], used_cards[1]]
        ret.sort()
        self.handle_hand_card_for_settle_show(ret)

    def record_peng_card(self, card_val):
        self.peng_card_vals.append([card_val, card_val, card_val])
        # 记录吃碰杠顺序 用于结束游戏显示

        self.handle_hand_card_for_settle_show([card_val, card_val, card_val])

    def record_dian_gang_card(self, source, card_val):
        self.dian_gang_card_vals.append([card_val, card_val, card_val, card_val])
        self.dian_gang_source[card_val] = source
        # 记录吃碰杠顺序 用于结束游戏显示
        self.handle_hand_card_for_settle_show([card_val, card_val, card_val, card_val])

    def record_bu_gang_card(self, card_val):
        self.bu_gang_card_vals.append([card_val, card_val, card_val, card_val])
        # 从碰牌记录中删除
        self.peng_card_vals.remove([card_val, card_val, card_val])

        # 记录吃碰杠顺序 用于结束游戏显示
        for i in range(len(self.hand_card_for_settle_show)-2):
            if self.hand_card_for_settle_show[i][0] == card_val:
                self.hand_card_for_settle_show[i].append(card_val)


    def record_an_gang_card(self, card_val):
        self.an_gang_card_vals.append([card_val, card_val, card_val, card_val])
        # 记录吃碰杠顺序 用于结束游戏显示
        self.handle_hand_card_for_settle_show([card_val, 0, 0, 0])


    def record_dian_hu_card(self, source, card_val):
        self.hu_source_seat_id = source

    def record_ting_info(self, chu_card_val, ting_info):
        self.ting_info_records.append({"chu": chu_card_val, "info": ting_info})

    def del_hand_card_by_val_list(self, card_val_list):
        for val in card_val_list:
            self.del_hand_card_by_val(val)

    def del_hand_card_by_val(self, card_val):
        self.del_hand_card_by_type(Card.cal_card_type(card_val), Card.cal_card_digit(card_val))

    def del_hand_card_by_type(self, card_type, card_digit):
        if not self.hand_card_info.get(card_type, None):
            return
        if 0 == self.hand_card_info[card_type][card_digit]:
            return
        self.hand_card_info[card_type][card_digit] -= 1
        self.hand_card_info[card_type][0] -= 1

    def add_hand_card_by_vals(self, card_vals=[]):
        if not card_vals:
            return
        for v in card_vals:
            card_type = Card.cal_card_type(v)
            card_digit = Card.cal_card_digit(v)
            self.hand_card_info[card_type][card_digit] += 1
            self.hand_card_info[card_type][0] += 1
        self.last_card_val = card_vals[-1]

    def union_hand_card(self):
        """
        将现有手牌联合在一起
        :return:
        """
        all_types = CardType.all_type()
        for t in all_types:
            self.union_card_info[t] = [0 for _ in range(CARD_SIZE[t])]

        tmp_hand_card = copy.deepcopy(self.hand_card_for_settle_show)
        for card_group in tmp_hand_card:
            if 4 == len(card_group):
                card_group[1] = card_group[0]
                card_group[2] = card_group[0]
                card_group[3] = card_group[0]
                card_group.pop()
            for card_val in card_group:
                if card_val:
                    card_type = Card.cal_card_type(card_val)
                    card_digit = Card.cal_card_digit(card_val)
                    self.union_card_info[card_type][card_digit] += 1
                    self.union_card_info[card_type][0] += 1

    def handle_hand_card_for_settle_show(self, card_lst=[]):
        if card_lst:
            sk = len(self.hand_card_for_settle_show) - 2
            self.hand_card_for_settle_show.insert(sk, card_lst)
        self.hand_card_for_settle_show[-2] = self.hand_card_vals
        if self.zi_mo:
            self.hand_card_for_settle_show[-2].remove(self.last_card_val)
            self.hand_card_for_settle_show[-1] = [self.last_card_val]
        self.union_hand_card()
