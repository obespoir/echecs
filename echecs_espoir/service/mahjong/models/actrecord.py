# coding=utf-8

import time


class ActRecord(object):
    """
    动作记录
    """
    def __init__(self, seat_id, act_type, cards, **kwargs):
        self.seat_id = seat_id
        self.act_type = act_type
        self.cards = cards             # 操作的牌
        self.gang_type = kwargs.get("gang_type", 0)  # 1: 补杠 2:暗杠  3:明杠
        self.act_time = time.time()

        self.change_point_list = []      # 该动作修改的玩家参数

    def set_change_point(self, change_point_list):
        self.change_point_list = change_point_list
