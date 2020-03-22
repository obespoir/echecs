# coding=utf-8


class ShunKeCardInfo(object):
    """
    手牌拆分成顺子和刻字的信息
    """
    def __init__(self):
        self.card_info = []      # 拆分的分组，最多2×7(七小对)，一般4×3+2, 十三幺之类的不使用该类
        self.shun_num = 0
        self.ke_num = 0
        self.jian_ke_num = 0
        self.feng_ke_num = 0

    def get_shun_ke_len(self):
        return len(self.card_info)

    # def is_info_over(self, row):
    #     if row > self.get_shun_ke_len():
    #         return True
    #     if len(self.card_info[row]) < 3:
    #         return True
    #     sum = self.card_info[row][0]