# coding=utf-8

__author__ = 'jamon'
import json

from service.mahjong.constants.gamedefine import Act
from service.mahjong.models.config.init_config import init_config_ins


class GameConfig(object):
    def __init__(self, game_type="default"):
        d_config = init_config_ins.all_config.get(game_type)
        self.test_mode = d_config.get("test_mode")                      # 一局游戏的玩家数
        self.max_player_num = d_config.get("max_player_num")            # 一局游戏的玩家数

        self.has_tong_pao = d_config.get("has_tong_pao")                # 是否可以通炮胡
        self.auto_act_list = d_config.get("auto_act_list")              # 自動操作列表, 按優先級降序排列
        self.is_hu_end = 1                                              # 是否胡牌后结束游戏

        # 检查动作相关　
        self.check_against_check_list = d_config.get("check_against_check_list")  # 出牌后检查其他玩家可进行的操作列表
        self.draw_card_check_list = d_config.get("draw_card_check_list")  # 摸牌后检查该玩家可进行的操作
        self.draw_card_bu_hua = d_config.get("draw_card_bu_hua")          # 摸牌时是否需要补花

        # 动作step相关　
        self.player_act_step = d_config["player_act_step"]
        self.draw_card_step = d_config.get("draw_card_step")
        self.start_game_sequence = d_config.get("start_game_sequence")   # 游戏开始时序列动作执行顺序
        self.player_act_hook = {Act.BU_GANG: [Act.DIAN_HU]}                                       # 玩家行为执行前钩子处理, 如抢杠胡{Act.BU_GANG: [Act.DIAN_HU], ...}

        # 牌型相关
        self.used_card_types = d_config.get("used_card_types")   # 使用的麻将牌花色
        self.used_hu_types = d_config.get("used_hu_types")        # 使用的麻将胡牌类型
        self.hu_fan_info = d_config.get("hu_fan_info")            # 各牌型番数信息
        self.mutex_list = d_config.get("mutex_list")              # 互斥牌型

        # 结算相关
        self.settle_gang_info = d_config.get("settle_gang_info")
        self.settle_fan_config = d_config.get("settle_fan_config") # 某玩家胡牌的计算公式为： y = (A(x+B)+C) * D
        self.gen_zhuang_fan = d_config.get("gen_zhuang_fan")         # 跟庄的番数，默认和屁胡基础番数一样

        # 是否具备过胡加倍
        self.pass_hu_double = 0

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~```")
        print(self.to_dict())

    def update_config(self, **kwargs):
        self.__dict__.update(**kwargs)
        special_rule = json.loads(self.special_rule)
        self.pass_hu_double = special_rule.get("pass_hu_double")

    def to_dict(self):
        return {
            "max_player_num": self.max_player_num,            # 一局游戏的玩家数
            "has_tong_pao": self.has_tong_pao,                # 是否可以通炮胡
            "auto_act_list": self.auto_act_list,              # 自動操作列表, 按優先級降序排列
            "is_hu_end": self.is_hu_end,                      # 是否胡牌后结束游戏

            "check_against_check_list": self.check_against_check_list,    # 出牌后检查其他玩家可进行的操作列表
            "draw_card_check_list": self.draw_card_check_list,          # 摸牌后检查该玩家可进行的操作
            "draw_card_bu_hua": self.draw_card_bu_hua,                  # 摸牌时是否需要补花

            "player_act_step": self.player_act_step,
            "draw_card_step": self.draw_card_step,
            "start_game_sequence": self.start_game_sequence,  # 游戏开始时序列动作执行顺序
            "player_act_hook": self.player_act_hook,          # 玩家行为执行前钩子处理, 如抢杠胡

            "used_card_types": self.used_card_types,          # 使用的麻将牌花色
            "used_hu_types": self.used_hu_types,              # 使用的麻将胡牌类型
            "hu_fan_info": self.hu_fan_info,                        # 各牌型番数信息
            "mutex_list": self.mutex_list,                    # 互斥牌型

            "settle_gang_info": self.settle_gang_info,
            "settle_fan_config": self.settle_fan_config,
            "gen_zhuang_fan": self.gen_zhuang_fan             # 跟庄的番数，默认和屁胡基础番数一样
        }

    def vars_to_dict(self):
        ret = {}
        for name, val in vars(self).items():
            ret[name] = val
        return ret

    def get_keep_card_num(self):
        """
        获取牌堆最少剩余牌数
        :return:
        """
        return 0


