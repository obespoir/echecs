# coding=utf-8

__author__ = 'jamon'


from service.mahjong.models.gamedata import GameData
from service.mahjong.models.playeract.player_act_manager import PlayerActManager
from service.mahjong.models.systemact.system_act_manager import SystemActManager
from service.mahjong.constants.gamedefine import SystemActType
from service.mahjong.models.timermanager import TimerManager, timer_manager_ins
from obespoir.share.ob_log import logger


class GameDesk(object):
    """
    游戏桌子流程控制器
    """
    def __init__(self, desk_id, custom_config=None, game_type="default"):
        self.desk_id = desk_id
        self.game_data = GameData(desk_id, custom_config=custom_config, game_type=game_type)

        # 系统行为流程执行顺序配置
        self.system_act_config = self.game_data.game_config.start_game_sequence

    def go_next_act(self, cur_flow, params={}):
        """
        执行下一步操作
        :param cur_flow: 当前操作类型， MahjongFlow
        :param params:  下一步操作需要的参数，json串传输
        :return:
        """
        if cur_flow not in self.system_act_config.keys():
            raise Exception("go_next_flow error:%s" % str([cur_flow, params]))

        next_act = self.system_act_config[cur_flow].get("next", None)
        if next_act:
            interval = self.system_act_config[cur_flow].get("interval", 0)
            if 0 < interval:
                TimerManager.call_later(interval, self.execute_system_act, next_act, params)
            else:
                self.execute_system_act(next_act, params)

    def start_game(self):
        # 重置game_data 中相关信息
        self.game_data.reset_players_data()
        self.go_next_act(SystemActType.START_GAME)
        for i in self.game_data.players:
            i.hand_card.reset_hand_card()


    def execute_system_act(self, act_type, act_params):
        """
        执行系统指定的行为
        :param act_type:
        :param act_params:
        :return:
        """
        logger.debug(u"execute_system_act: %s", [act_type, act_params])
        ret = SystemActManager.get_instance(self.desk_id).system_act(act_type, act_params=act_params)
        self.go_next_act(act_type)

    def handle_player_act(self, seat_id, act_type, act_params):
        """
        玩家选择进行的操作
        :param seat_id:
        :param act_type:
        :param act_params:
        :return:
        """
        logger.debug(u"handle_player_act: %s", [seat_id, act_type, act_params])
        return PlayerActManager.get_instance(self.desk_id).player_act(seat_id, act_type, act_params)

    def get_all_info_of_player(self, seat_id):
        """
        获取指定玩家在当局游戏中的所有信息
        :param seat_id:
        :return:
        """
        return {
            "player_info": self.game_data.get_all_player_info(seat_id),
            "desk_info": self.game_data.get_desk_info(),
            "wait_task": self.game_data.get_wait_task(seat_id)
        }

    def handler_test_act(self, seat_id, act, card_list):
        """
        测试接口
        :param seat_id:
        :param act:
        :param card_list:
        :return:
        """
        return PlayerActManager.get_instance(self.desk_id).test_act(seat_id, act, card_list)

    def end_game(self):
        for i in range(self.game_data.max_player_num):
            timer_manager_ins.kill_timer(self.desk_id, i, is_force=True)

