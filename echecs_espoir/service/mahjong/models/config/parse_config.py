# coding=utf-8

from service.mahjong.constants.carddefine import HuType
from service.mahjong.constants.gamedefine import Act, HuSettleParamType, SettleHuFan, SystemActType, GangType
from obespoir.share.parse_json import ParseJson


class ParseConfig(object):
    """
    游戏配置解析
    """
    def __init__(self):
        self.game_parse = GameParse()
        self.player_act_parse = PlayerActParse()
        self.system_act_parse = SystemActParse()

    def parse(self, config_path):
        parse_json = ParseJson.loads(config_path)
        ret = {}
        game_result = self.game_parse.parse(parse_json.get("game", {}))
        if game_result:
            ret.update(game_result)
        player_act_result = self.player_act_parse.parse(parse_json.get("player_act", {}))
        if player_act_result:
            ret.update(player_act_result)
        system_act_result = self.system_act_parse.parse(parse_json.get("system_act", {}))
        if system_act_result:
            ret.update(system_act_result)

        return ret


class GameParse(object):

    def __init__(self):
        # 需要对配置进行特殊处理的选项
        self.handler = {
            "used_hu_types": self.parse_used_hu_types,
            "hu_fan_info": self.parse_hu_fan_info,
            "start_game_sequence": self.parse_start_game_sequence,
            "player_act_hook": self.parse_player_act_hook
        }

    def parse(self, game_json):
        ret = {}
        for k, v in game_json.items():
            if k in self.handler.keys():
                ret[k] = self.handler.get(k)(v)
            else:
                ret[k] = v
        return ret

    def parse_used_hu_types(self, used_hu_types):
        ret = {}
        for k, v in used_hu_types.items():
            ret[HuType.get_type(k)] = v
        return ret

    def parse_hu_fan_info(self, fan_json):
        print("parse_hu_fan_info, fan_json=", fan_json)
        ret = {}
        for k, v in fan_json.items():
            ret[HuType.get_type(k)] = v
        print("parse_hu_fan_info, ret=", ret)
        return ret

    def parse_start_game_sequence(self, start_json):
        ret = {}
        for k, v in start_json.items():
            ret[SystemActType.get_type(k)] = v
        return ret

    def parse_player_act_hook(self, hook_json):
        ret = {}
        for k, v in hook_json.items():
            ret[Act.get_type(k)] = v
        return ret


class PlayerActParse(object):

    def __init__(self):
        pass

    def parse(self, act_json):
        ret = {}
        for k, v in act_json.items():
            ret[Act.get_type(k)] = v.get("step")
        return {"player_act_step": ret}


class SystemActParse(object):

    def __init__(self):
        # 需要对配置进行特殊处理的选项
        self.handler = {
            "check_against": self.parse_check_against,
            "draw_card": self.parse_draw_card,
            "settle": self.parse_settle
        }

    def parse(self, act_json):
        ret = {}
        for k, v in act_json.items():
            if k in self.handler.keys():
                ret.update(self.handler.get(k)(v))
            else:
                ret.update(v)
        return ret

    def parse_check_against(self, params):
        ret = {}
        if "check_list" in params.keys():
            ret["check_against_check_list"] = params["check_list"]
        return ret

    def parse_draw_card(self, params):
        ret = {}
        if "check_list" in params.keys():
            ret["draw_card_check_list"] = params["check_list"]
        if "step" in params.keys():
            ret["draw_card_step"] = params['step']
        if "bu_hua" in params.keys():
            ret["draw_card_bu_hua"] = params["bu_hua"]
        return ret

    def parse_settle(self, params):
        ret = {}
        if "gang_info" in params.keys():
            ret["settle_gang_info"] = self.parse_settle_gang_info(params["gang_info"])
        if "fan_config" in params.keys():
            ret['settle_fan_config'] = self.parse_settle_fan_config(params["fan_config"])
        if "gen_zhuang_fan" in params.keys():
            ret["gen_zhuang_fan"] = params["gen_zhuang_fan"]
        return ret

    def parse_settle_gang_info(self, gang_json):
        ret = {}
        for k, v in gang_json.items():
            ret[GangType.get_type(k)] = v
        return ret

    def parse_settle_fan_config(self, fan_json):
        ret = {}
        for k, v in fan_json.items():
            param_type = HuSettleParamType.get_type(k)
            info = {}
            for t, fan in v.items():
                info[SettleHuFan.get_type(t)] = fan
            ret[param_type] = info
        return ret


parse_config_ins = ParseConfig()


if __name__ == "__main__":
    b = {u'YiSeSiTongShun': 48, u'ShuangAnKe': 2, u'PingHu': 2, u'DiHu': 88, u'YiSeShuangLongHui': 64,
         u'JiuLianBaoDeng': 88, u'XiaoSanYuan': 64, u'MingGang': 1, u'HaiDiLaoY': 8, u'TianHu': 88,
         u'MiaoShouHuiChun': 8, u'MenQianQing': 2, u'ShuangJianKe': 6, u'DanGouJiang': 1, u'HunYiSe': 6,
         u'YiSeSanJieGao': 24, u'DaSiXi': 88, u'ZiYiSe': 64, u'XiaoSiXi': 64, u'AnGang': 2, u'ShuangMingGang': 4,
         u'BaoTing': 2, u'SanAnKe': 16, u'QingYiSe': 24, u'QuanDaiYao': 4, u'HunYaoJiu': 32, u'SanFengKe': 12,
         u'YiSeSiBuGao': 32, u'YiBanGao': 1, u'ZiMo': 1, u'YiSeSanTongShun': 24, u'DuanYao': 2, u'QuanQiuRen': 6,
         u'QiXiaoDui': 24, u'QiangGangHu': 8, u'SiGang': 88, u'BianZhang': 1, u'SiAnKe': 64, u'SiGuiYi': 2,
         u'YiSeSiJieGao': 48, u'SanGang': 32, u'ShuangAnGang': 8, u'JianKe': 2, u'PengPengHu': 6, u'BuQiuRen': 4,
         u'RenHu': 64, u'YiSeSanBuGao': 16, u'LianLiu': 1, u'GangShangKaiHua': 8, u'HuJueZhang': 4, u'TianTing': 32,
         u'QingLong': 16, u'PiHu': 1, u'LaoShaoFu': 1, u'YaoJiuKe':1, u'DaSanYuan': 88}
    gp = GameParse()

    gp.parse_hu_fan_info(b)