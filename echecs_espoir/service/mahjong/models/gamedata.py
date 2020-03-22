# coding=utf-8

__author__ = 'jamon'

from service.mahjong.models.config.gameconfig import GameConfig
from service.mahjong.constants.gamedefine import GameStatus, Act
from service.mahjong.constants.carddefine import BLACK
from service.mahjong.models.utils.cardanalyse import CardAnalyse
from service.mahjong.models.card.carddealer import CardDealer
from service.mahjong.models.hutype.typemanager import HuTypeManager, HuType
from service.mahjong.models.player import Player
from service.mahjong.models.callbackmanager import CallbackFuncType
from service.mahjong.models.timermanager import timer_manager_ins
from service.mahjong.models.state_machine import StateMachine
from share.message_ids import PUSH_CALL_CARD


class RoundData(object):
    """
    当轮数据信息
    """
    def __init__(self, max_play_num=1, cur_play_num=1, player_num=4):
        """
        :param max_play_num:   当轮最多玩多少局
        :param cur_play_num:   当前正在玩第多少局
        """
        self.player_num = player_num
        self.max_play_num = max_play_num            # 当轮最多玩多少局
        self.cur_play_num = cur_play_num            # 当前正在玩第多少局
        self.points = [0 for _ in range(player_num)]       # 当前当轮积分情况

    def reset(self):
        self.max_play_num = 1  # 当轮最多玩多少局
        self.cur_play_num = 1  # 当前正在玩第多少局
        self.points = [0 for _ in range(self.player_num)]  # 当前当轮积分情况


class GameData(object):
    """
    当次游戏全局数据
    """
    def __init__(self, desk_id, custom_config=None, game_type="default"):
        self.desk_id = desk_id
        self.game_config = GameConfig(game_type=game_type)
        print("custom_config=", custom_config)
        if custom_config:
            self.game_config.update_config(**custom_config)

        self.card_dealer = CardDealer(c_types=self.game_config.used_card_types)

        # 牌值分析器
        self.card_analyse = CardAnalyse(card_type_list=self.game_config.used_card_types, base_hu_type=self.game_config.used_hu_types)
        # 胡牌类型管理器
        self.hu_manager = HuTypeManager(self.game_config, card_analyse=self.card_analyse)

        self.game_status = GameStatus.WAIT_AGREE
        self.players = [Player(seat_id=i, game_data=self) for i in range(self.max_player_num)]

        self.banker_seat_id = -1         # 庄家座位号
        self.hu_player_static = {}       # 当次已胡牌玩家统计（不存血战中当局的历史胡牌信息）
                                         # {seat_id:{type:[], is_zi_mo:0/1, source:int, card:int}, ...}

        self.last_chu_card_val = BLACK   # 最近一次出的牌
        self.cur_deal_card_val = BLACK   # 当前牌局上正在操作的那张牌
        self.last_chu_card_seat_id = -1  # 最近一次出牌玩家的位置
        self.last_get_card_val = [BLACK, BLACK, BLACK, BLACK]  # 最近一次某位置玩家获得的牌
        self.next_speaker_callback = {}  # 接下来玩家待进行的操作（其他玩家都选择过时）
                                            # {type: CallbackFuncType, seat_id: int, call_params: {}}

        self.cur_players_to_act = {}     # 当前所有玩家待进行的操作
                                         # {seat_id:{Act.HU:{}, Act.PENG:{}, ...}, seat_id: []}
        self.cur_players_acted = {}      # 当前出牌轮次所有玩家已经作出响应的玩家操作
                                         # {seat_id:{"act_type":Act.HU, "params":act_params},...}

        self.settle_data = {}            # 当局游戏输赢情况 {total_points:[],
                                         # detail:[{type:int, points:[,...,], params:{}}, ...]}

        self.yi_chu_card_vals = []       # 当局已出的牌, 所有玩家都可见的牌
        self.dealed_card_vals = []       #

        self.act_record_list = []        # 当局动作记录

        self.test_sure_next_card = [BLACK for _ in range(self.max_player_num)]    # 测试接口使用：指定下一张牌

        self.round_info = RoundData(player_num=self.game_config.max_player_num)

        self.state_machine = StateMachine(self)


    @property
    def max_player_num(self):
        return self.game_config.max_player_num

    def get_all_player_info(self, seat_id):
        """
        某玩家获取当前桌子中所有玩家的信息
        :param seat_id:
        :return:
        """
        player_info = [{} for _ in range(self.max_player_num)]
        is_god_perspective = self.players[seat_id].hand_card.is_ting and self.game_config.pass_hu_double
        for i, player in enumerate(self.players):
            is_own = True if i == seat_id else False
            if player:
                player_info[i] = player.hand_card.to_dict_for_reconnect(is_own, is_god_perspective)

        return player_info

    def get_desk_info(self):
        return {
            "desk_id": self.desk_id,
            # "game_config": self.game_config.vars_to_dict(),
            "room_type": self.game_config.vars_to_dict().get("room_type"),
            "status": self.game_status,
            "bank_seat_id": self.banker_seat_id,
            "remain_count": self.card_dealer.card_count
        }

    def reset_game_data(self):
        """
        重置清空上局的游戏相关数据s
        :return:
        """
        self.game_status = GameStatus.WAIT_AGREE
        self.card_dealer.clear_data()
        self.hu_player_static = {}  # 当次已胡牌玩家统计（不存血战中当局的历史胡牌信息）
        # {seat_id:{type:[], is_zi_mo:0/1, source:int, card:int}, ...}

        self.cur_speaker_seat_id = -1  # 当前说话的玩家
        self.last_chu_card_val = BLACK  # 最近一次出的牌
        self.cur_deal_card_val = BLACK   # 当前牌局上正在操作的那张牌
        self.last_chu_card_seat_id = -1  # 最近一次出牌玩家的位置
        self.next_speaker_callback = {}  # 接下来玩家待进行的操作（其他玩家都选择过时）
        # {type: CallbackFuncType, seat_id: int, call_params: {}}

        self.cur_players_to_act = {}  # 当前所有玩家待进行的操作
        # {seat_id:{Act.HU:{}, Act.PENG:{}, ...}, seat_id: []}
        self.cur_players_acted = {}  # 当前出牌轮次所有玩家已经作出响应的玩家操作
        # {seat_id:{Act.HU:act_params, ...},...}

        self.settle_data = {}  # 当局游戏输赢情况 {total_points:[],
        # detail:[{type:int, points:[,...,], params:{}}, ...]}

        self.yi_chu_card_vals = []  # 当局已出的牌, 所有玩家都可见的牌
        self.dealed_card_vals = []  #

        self.act_record_list = []  # 当局动作记录



    def reset_players_data(self):
        # 重置用户信息
        for i in self.players:
            i.reset_data()


    def reset_round_data(self):
        """一轮结束"""
        self.round_info.reset()
        self.banker_seat_id = -1

    def get_next_seat_id(self, cur_seat_id):
        return (cur_seat_id+1) % self.max_player_num

    def is_player_auto(self, seat_id):
        if self.players[seat_id]:
            return self.players[seat_id].is_auto
        return 0

    def reset_hu_static(self):
        self.hu_player_static = {}

    def update_hu_static(self, seat_id, params={}):
        """更新已胡牌信息"""
        if seat_id in self.hu_player_static.keys():
            self.hu_player_static[seat_id].update(params)
        else:
            self.hu_player_static[seat_id] = params

    def get_player_can_speaker(self, seat_id):
        return self.cur_players_to_act.get(seat_id, {})

    def get_min_left_cards(self):
        """
        获取牌堆中最少剩余的牌数
        :return:
        """
        return 1

    def add_player_to_act(self, seat_id, act_type, act_params={}):
        """
        添加玩家可进行的操作
        :param seat_id:
        :param act_type:
        :param act_params:
        :return:
        """
        if seat_id in self.cur_players_to_act.keys():
            self.cur_players_to_act[seat_id][act_type] = act_params
        else:
            self.cur_players_to_act[seat_id] = {act_type: act_params}

    def del_player_to_act(self, seat_id):
        """
        删除玩家可进行的操作
        :param seat_id:
        :param act_type:
        :return:
        """
        if seat_id not in self.cur_players_to_act.keys():
            return 1

        self.cur_players_to_act.pop(seat_id)
        return 1

    def add_player_acted(self, seat_id, act_type, act_params={}):
        """
        添加玩家已进行的操作
        :param seat_id:
        :param act_type:
        :param act_params:
        :return:
        """
        self.cur_players_acted[seat_id] = {act_type: act_params}

    def add_settle_info(self, settle_type, seat_points=[], params={}):
        """
        添加结算变化点数
        :param seat_points:
        :return:
        """
        if not self.settle_data:
            self.settle_data = {"total_points": [0 for i in range(self.max_player_num)], "detail": []}
        for i in range(self.max_player_num):
            self.settle_data["total_points"][i] += seat_points[i]
        self.settle_data["detail"].append({"type": settle_type, "points": seat_points, "params":params})

    def add_chu_card(self, card_val):
        if isinstance(card_val, list):
            for i in card_val:
                self.yi_chu_card_vals.append(i)
        else:
            self.yi_chu_card_vals.append(card_val)

    def get_wait_task(self, seat_id):
        ret = {}
        timer = timer_manager_ins.get_timer(self.desk_id, seat_id)
        if timer:
            if CallbackFuncType.FUNC_AUTO_PLAYER_ACT == timer["call_type"]:
                ret = {"end_time": timer["end_time"], "params": timer['params'], "command_id": PUSH_CALL_CARD}
        print("get_wait_task=", ret)
        return ret

    def get_all_chu_cards(self):
        """获取当局所有玩家已出过的牌"""
        ret = []
        for i in range(self.max_player_num):
            hand_card = self.players[i].hand_card
            ret.extend(hand_card.out_card_vals)
            ret.extend(hand_card.chi_card_vals)
            ret.extend(hand_card.peng_card_vals)
            ret.extend(hand_card.dian_gang_card_vals)
            ret.extend(hand_card.bu_gang_card_vals)
        return ret
