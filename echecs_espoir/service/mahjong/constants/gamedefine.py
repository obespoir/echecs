# coding=utf-8

__author__ = 'jamon'


class GameStatus(object):
    """游戏状态"""
    WAIT_SET   = 1
    WAIT_AGREE = 2
    PLAYING    = 3
    OVER       = 4


class Act(object):
    """
    动作类型， 数值大小是用来表示相对关系，数值内容本身不具备意义
    """
    GUO     = 0
    CHU     = 10
    CHI     = 20
    PENG    = 30
    DIAN_GANG = 40
    BU_GANG = 50
    AN_GANG = 60
    TING    = 70
    DIAN_HU = 80
    ZI_MO = 90
    WAITE_ANSWER = 100
    GUO_HU_DOUBLE = 110

    @classmethod
    def to_dict(cls):
        return {
            "guo": cls.GUO,
            "chu": cls.CHU,
            "chi": cls.CHI,
            "peng": cls.PENG,
            "dian_gang": cls.DIAN_GANG,
            "bu_gang": cls.BU_GANG,
            "an_gang": cls.AN_GANG,
            "ting": cls.TING,
            "dian_hu": cls.DIAN_HU,
            "zi_mo": cls.ZI_MO
        }

    @classmethod
    def get_type(cls, act_name):
        return cls.to_dict().get(act_name)


class TimerType(object):
    """定时器类型"""
    NORMAL = 0
    KEEP   = 1


class SettleType(object):
    "结算类型"
    HU           = 1     # 胡牌结算
    GANG         = 2     # 杠
    GEN_ZHUANG   = 3     # 跟庄
    DRAW         = 4     # 平局


class GangType(object):
    "杠类型"
    DIAN_GANG    = 1     # 点杠
    BU_GANG      = 2     # 补杠
    AN_GANG      = 3     # 暗杠

    @classmethod
    def to_dict(cls):
        return {
            "dian_gang": cls.DIAN_GANG,
            "bu_gang": cls.BU_GANG,
            "an_gang": cls.AN_GANG
        }

    @classmethod
    def get_type(cls, name):
        return cls.to_dict().get(name)


class SystemActType(object):
    START_GAME   = 1        # 开始游戏
    GEN_BANK     = 2        # 定庄
    DEAL_CARD    = 3        # 发牌
    DRAW_CARD     = 4       # 摸牌
    CHECK_AGAINST = 5       # 检查其他玩家可进行的操作
    SETTLE = 6              # 游戏结算
    GAME_OVER = 7           # 游戏结束
    WAITE_ANSWER = 8        # 游戏发牌后等待玩家摸牌

    @classmethod
    def to_dict(cls):
        return {
            "start_game": cls.START_GAME,
            "gen_bank": cls.GEN_BANK,
            "deal_card": cls.DEAL_CARD,
            "draw_card": cls.DRAW_CARD,
            "check_against": cls.CHECK_AGAINST,
            "settle": cls.SETTLE,
            "game_over": cls.GAME_OVER,
            "waite_answer": cls.WAITE_ANSWER
        }

    @classmethod
    def get_type(cls, name):
        return cls.to_dict().get(name)


class CheckAgainType(object):
    """某次出牌后，检查其他玩家可进行的操作配置项"""
    CAN_CHI = 1             # 可吃
    CAN_PENG = 2            # 可碰
    CAN_DIAN_PAO = 3        # 可点炮
    CAN_DIAN_GANG = 4       # 可点杠

    @classmethod
    def to_dict(cls):
        return {
            "can_chi": cls.CAN_CHI,
            "can_peng": cls.CAN_PENG,
            "can_dian_pao": cls.CAN_DIAN_PAO,
            "can_dian_gang": cls.CAN_DIAN_GANG
        }


class CheckSelfActType(object):
    """检查摸牌后自身可以进行的动作配置"""
    CAN_AN_GANG = 1         # 可暗杠
    CAN_BU_GANG = 2         # 可补杠
    CAN_ZI_MO = 3           # 可自摸
    CAN_TING = 4            # 可听

    @classmethod
    def to_dict(cls):
        return {
            "can_an_gang": cls.CAN_AN_GANG,
            "can_bu_gang": cls.CAN_BU_GANG,
            "can_zi_mo": cls.CAN_ZI_MO,
            "can_ting": cls.CAN_TING
        }


class CheckNameTypeRel(object):
    """检查摸牌后自身动作名称和类型对应关系"""
    REL = {
        CheckSelfActType.CAN_AN_GANG: Act.AN_GANG,
        CheckSelfActType.CAN_BU_GANG: Act.BU_GANG,
        CheckSelfActType.CAN_ZI_MO: Act.ZI_MO,
        CheckSelfActType.CAN_TING: Act.TING
    }


class SettleHuFan(object):
    """胡结算时番数加成的类型"""
    ZHUANG = 1      # 庄
    DIAN_GANG = 2   # 点杠
    BU_GANG = 3     # 补杠
    AN_GANG = 4     # 暗杠
    JIA_MA = 5      # 加码
    JIA_PIAO = 6    # 加漂
    HUA = 7         # 花

    LIANG_DAO = 8   # 亮倒
    GUO_HU = 9      # 过胡加倍

    GANG_SHANG_PAO = 10         # 杠上炮
    GANG_SHANG_KAI_HUA = 11     # 杠上开花
    QIANG_BU_GANG_HU = 12       # 抢杠胡

    @classmethod
    def to_dict(cls):
        return {
            "zhuang": cls.ZHUANG,
            "dian_gang": cls.DIAN_GANG,
            "bu_gang": cls.BU_GANG,
            "an_gang": cls.AN_GANG,
            "jia_ma": cls.JIA_MA,
            "jia_piao": cls.JIA_PIAO,
            "hua": cls.HUA,
            "liang_dao": cls.LIANG_DAO,
            "guo_hu": cls.GUO_HU,
            "gang_shang_pao": cls.GANG_SHANG_PAO,
            "gang_shang_kai_hua": cls.GANG_SHANG_KAI_HUA,
            "qiang_bu_gang_hu": cls.QIANG_BU_GANG_HU
        }

    @classmethod
    def get_type(cls, name):
        return cls.to_dict().get(name)


class HuSettleParamType(object):
    A = 1
    B = 2
    C = 3
    D = 4

    @classmethod
    def to_dict(cls):
        return {
            "A": cls.A,
            "B": cls.B,
            "C": cls.C,
            "D": cls.D
        }

    @classmethod
    def get_type(cls, name):
        return cls.to_dict().get(name)


class GameActStatus(object):
    # 當前遊戲中最近的動作狀態
    NOTHING = 0
    AFTER_CHU_CARD = 1         # 已出牌
    AFTER_DRAW_CARD = 2           # 已摸牌


class TestActionType(object):
    HUAN_CARD = 1
    SURE_NEXT_CARDS = 2
    GET_LAST_CARD = 3
    INIT_DRAW_CARDS = 4
    QUICK_DRAW = 5
