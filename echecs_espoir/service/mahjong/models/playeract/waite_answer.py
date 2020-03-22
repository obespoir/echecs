# coding=utf-8

from service.mahjong.models.playeract.base_player_act import BasePlayerAct
from obespoir.share.ob_log import logger


class WaiteAnswer(BasePlayerAct):
    """
    初始发牌
    """
    def __init__(self, game_data):
        super(WaiteAnswer, self).__init__(game_data=game_data)

    def execute(self):
        """
        庄家摸牌前处理_ 此处可用来处理加漂之类的(由于前段动画不放时间不定, 需要等待前端动画播放完毕在给庄家发牌)
        :return:
        """
        logger.debug(u"等待玩家发牌动画处理完毕: %s", str([]))

        self.draw_card(self.game_data.banker_seat_id)
        # print "cur_players_to_act", self.game_data.cur_players_to_act
        # print "cur_players_acted", self.game_data.cur_players_acted
        # for i in range(self.game_data.max_player_num):
        #     if self.game_data.cur_players_to_act.get(i):
        #         if self.game_data.cur_players_to_act[i].get(100, -1) != -1:
        #             del(self.game_data.cur_players_to_act[i][100])
        #     if self.game_data.cur_players_acted.get(i):
        #         if self.game_data.cur_players_acted[i].get(100, -1) != -1:
        #             del(self.game_data.cur_players_acted[i][100])
        # print "WaiteAnswer cur_players_to_act:", self.game_data.cur_players_to_act
        # print "WaiteAnswer cur_players_acted:", self.game_data.cur_players_acted

        return 1


