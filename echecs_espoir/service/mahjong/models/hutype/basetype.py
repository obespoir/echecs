# coding=utf-8


class BaseType(object):
    """
    基础胡牌类型
    """
    def __init__(self):
        super(BaseType, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        """
        判断是否该胡牌类型
        :param hand_card: 判断的手牌，矩阵表示
        :param card_analyse: 牌型分析器, CardAnalyse对象
        :return: 0: 不是, 1：是
        """
        pass

