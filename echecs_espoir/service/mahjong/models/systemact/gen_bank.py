# coding=utf-8

from share import message_ids
from service.mahjong.constants.gamedefine import GameStatus
from service.mahjong.controls.notifybridge import notify_all_desk_player
from service.mahjong.models.systemact.base_system_act import BaseSystemAct
from obespoir.share.ob_log import logger

import random


class GenBank(BaseSystemAct):
    """
    定庄
    """
    def __init__(self, game_data):
        super(GenBank, self).__init__(game_data=game_data)

    def execute(self):
        """
        定庄
        :return:
        """
        logger.debug(u"定庄: %s", str([]))
        dice = []
        if -1 == self.game_data.banker_seat_id:
            # 初始时
            dice = self.get_random_dice()
            self.game_data.banker_seat_id = (dice[0]+dice[1]-1) % self.max_player_num
        else:
            if not self.game_data.hu_player_static:
                # 上局为流局/荒庄, 则随机定庄
                dice = self.get_random_dice()
                self.game_data.banker_seat_id = (dice[0] + dice[1] - 1) % self.max_player_num
            else:
                source = -1
                for seat_id, params in self.game_data.hu_player_static.items():
                    self.game_data.banker_seat_id = seat_id
                    source = params.get("source", -1)
                if 1 < len(self.game_data.hu_player_static):
                    # 一炮多响, 点炮的人做庄
                    if -1 == source:
                        logger.error("gen_banker error: %s", str(self.game_data.hu_player_static))
                        raise Exception()
                    self.game_data.banker_seat_id = source
        # 重置胡牌相关信息
        self.game_data.reset_hu_static()

        notify_all_desk_player(self.desk_id, message_ids.PUSH_GEN_BANK,
                               data={"bank_seat_id": self.game_data.banker_seat_id, "dice": dice})
        # 清理上一局信息
        self.game_data.reset_game_data()
        # 洗牌
        self.card_dealer.shuffle_card()
        # 将庄家位置存入game_data
        self.game_data.last_chu_card_seat_id = self.game_data.banker_seat_id


    def get_random_dice(self):
        return [random.randint(1, 6) for _ in range(2)]




