# coding=utf-8

from service.mahjong.constants.carddefine import CardType, CARD_SIZE, BLACK
from service.mahjong.models.card.card import Card
from random import randint


class CardDealer(object):
    """
    发牌器
    """
    def __init__(self, c_types=[]):
        """
        :param c_types:  花色类型
        """
        self.types = c_types  # [1, 4, 5, 6]  万, 风, 箭, 花
        self.all_card_vals = []
        self.card_count = 0
        self.left_index = 0         # 两个指针，一个头一个尾
        self.right_index = -1

        self.clear_data()

    def clear_data(self):
        self.card_count = 0
        self.all_card_vals = []

        for t in self.types:
            for d in range(1, CARD_SIZE[t]):
                for k in range(0, 4 if t != CardType.HUA else 1):
                    self.all_card_vals.append(Card.cal_card_val(t, d))
                    self.card_count += 1
        self.left_index = 0
        self.right_index = self.card_count - 1

    def shuffle_card(self):
        for i in range(0, 7):
            for j in range(0, self.card_count-1):
                random_num = randint(j+1, self.card_count-1)
                self.all_card_vals[j], self.all_card_vals[random_num] = self.all_card_vals[random_num], self.all_card_vals[j]

    def is_has_card(self):
        return self.card_count > 0

    def draw_cards(self, num=1, is_last=False):

        cards = []
        for i in range(num):
            c = self.draw_a_card(is_last=is_last)
            if c:
                cards.append(c)
        return cards

    def draw_a_card(self, is_last=False):
        """
        从牌堆摸牌
        :param is_last:
        :return:
        """
        if not self.is_has_card():
            return BLACK
        print("draw_a_card:", self.card_count)
        card_val = BLACK
        if is_last:
            while self.all_card_vals[self.left_index] == BLACK:
                self.left_index += 1

            card_val = self.all_card_vals[self.left_index]
            self.all_card_vals[self.left_index] = BLACK
            self.left_index += 1
        else:
            while self.all_card_vals[self.right_index] == BLACK:
                self.right_index -= 1

            card_val = self.all_card_vals[self.right_index]
            self.all_card_vals[self.right_index] = BLACK
            self.right_index -= 1

        self.card_count -= 1
        return card_val

    def draw_a_card_first_without_hua(self, is_last=False, test_mode=1, seat_id=0,card_list=[]):
        """

        :param is_last:
        :return:
        """

        if not self.is_has_card():
            return BLACK
        print("draw_a_card_first_without_hua:", self.card_count)
        card_val = BLACK
        if test_mode and card_list[seat_id]:
            card_val = card_list[seat_id].pop()
        else:
            if is_last:
                while self.all_card_vals[self.left_index] == BLACK:
                    self.left_index += 1

                card_val = self.all_card_vals[self.left_index]
                self.all_card_vals[self.left_index] = BLACK
                self.left_index += 1
            else:
                while self.all_card_vals[self.right_index] == BLACK:
                    self.right_index -= 1

                card_val = self.all_card_vals[self.right_index]
                # 处理首张发牌是花牌的情况
                # if self.card_count == 42:
                #     card_type = Card.cal_card_type(card_val)
                #     if card_type == CardType.HUA:
                #         index_unhua = 0
                #         while self.all_card_vals[index_unhua] != BLACK and Card.cal_card_type(self.all_card_vals[index_unhua]) == CardType.HUA:
                #             index_unhua +=1
                #         unhua_card = self.all_card_vals[index_unhua]
                #         self.all_card_vals[index_unhua] = card_val
                #         card_val = unhua_card
                #         print "first card is a hua!! card_val=",card_val

                self.all_card_vals[self.right_index] = BLACK
                self.right_index -= 1

        self.card_count -= 1
        return card_val

    def get_the_last_card(self):
        return self.all_card_vals[self.left_index]

    @property
    def get_remain_count(self):
        return self.card_count

