# coding=utf-8

from service.mahjong.models.card.hand_card import HandCard
from service.mahjong.constants.gamedefine import Act


class Player(object):
    """
    游戏内玩家类
    """
    def __init__(self, seat_id, game_data, point=0):
        self.game_data = game_data
        self.seat_id = seat_id
        self.hu_source_seat = -1    # 胡牌来源座位号
        self.can_hu_result = []     # 玩家当前可胡的牌型

        self.hand_card = HandCard(seat_id, game_data)
        self.point = point

        self.time_out_count = 0     # 超时次数
        self.is_auto = 0            # 是否处于托管状态

        self.zi_mo_num = 0
        self.hu_pai_num = 0
        self.jie_pao_num = 0
        self.dian_pao_num = 0
        self.an_gang_num = 0
        self.ming_gang_num = 0


        self.hook_hu_seat_id = -1  # 抢胡来源座位id

        self.ting_info = {}     # 选择听牌后的胡牌信息 {胡的牌:{"fan":胡牌基本类型番数, "type_list":[胡牌类型]}, ...}
        self.can_ting_info = {}    # 可以听牌的信息  {出牌１：{胡的牌:{"fan":胡牌基本类型番数, "type_list":[胡牌类型]}, ...}

    def reset_data(self):
        """
        一局游戏结束重置玩家数据
        :return:
        """
        self.hu_source_seat = -1  # 胡牌来源座位号
        self.hand_card = HandCard(self.seat_id, self.game_data)

        self.time_out_count = 0  # 超时次数
        self.is_auto = 0  # 是否处于托管状态

        self.zi_mo_num = 0
        self.hu_pai_num = 0
        self.jie_pao_num = 0
        self.dian_pao_num = 0
        self.an_gang_num = 0
        self.ming_gang_num = 0

        self.ting_info = {}
        self.can_ting_info = {}

        self.reset_hook()

    def set_hand_card(self, hand_card):
        self.hand_card.hand_card_info = hand_card

    def change_point(self, num):
        self.point += num

    def chu_card(self, card_val):
        self.hand_card.del_hand_card_by_val(card_val)
        self.hand_card.out_card_vals.append(card_val)

    def reset_hook(self):
        self.hook_hu_seat_id = -1  # 抢胡来源座位id

    def set_can_ting_info(self, ting_info={}):
        """
        记录可听牌信息
        :param ting_info:  可以听牌的信息 {出牌１：{胡的牌:{"fan":胡牌基本类型番数, "type_list":[胡牌类型]}, ...}
        :return:
        """
        self.can_ting_info = ting_info

    def set_ting_info(self, chu_card_val):
        """
        记录选择的听牌信息
        :param chu_card_val: 选择打出哪张牌后听牌
        :return:
        """
        self.ting_info = self.can_ting_info.get(chu_card_val)
