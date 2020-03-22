# coding=utf-8

CARD_DIGIT = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九"]
WAN_DESC = ["零", "一万", "二万", "三万", "四万", "五万", "六万", "七万", "八万", "九万"]
TIAO_DESC = ["零", "一条", "二条", "三条", "四条", "五条", "六条", "七条", "八条", "九条"]
BING_DESC = ["零", "一饼", "二饼", "三饼", "四饼", "五饼", "六饼", "七饼", "八饼", "九饼"]
FENG_DESC = ["零", "东风", "南风", "西风", "北风"]
JIAN_DESC = ["零", "中", "发", "白"]
HUA_DESC = ["零", "春", "夏", "秋", "冬", "梅", "兰", "竹", "菊"]
CARD_NAME = ["暗牌", "万", "条", "饼", "风", "箭", "花"]
BLACK = 0    # 暗牌
LAI_ZI = 10000    # 癞子


class CardType(object):
    DARK = 0            # 暗牌
    WAN  = 1            # 万
    TIAO = 2            # 条
    BING = 3            # 饼
    FENG = 4            # 风
    JIAN = 5            # 箭
    HUA  = 6            # 花

    @staticmethod
    def is_valid_type(card_type):
        return card_type in [CardType.WAN, CardType.BING, CardType.TIAO,
                             CardType.FENG, CardType.JIAN, CardType.HUA]

    @staticmethod
    def all_type():
        return [CardType.WAN, CardType.BING, CardType.TIAO,
                             CardType.FENG, CardType.JIAN, CardType.HUA]


CARD_SIZE = {CardType.WAN: 10, CardType.TIAO: 10, CardType.BING: 10, CardType.FENG: 5,
             CardType.JIAN: 4, CardType.HUA: 9, CardType.DARK: 1}
CARD_DESC_TABLE = {
    CardType.WAN: WAN_DESC, CardType.TIAO: TIAO_DESC, CardType.BING: BING_DESC,
    CardType.FENG: FENG_DESC,
    CardType.JIAN: JIAN_DESC, CardType.HUA:HUA_DESC, CardType.DARK: [["暗牌"]]
}


class Digits(object):
    ZERO   = 0
    ONE    = 1
    TWO    = 2
    THREE  = 3
    FOUR   = 4
    FIVE   = 5
    SIX    = 6
    SEVEN  = 7
    EIGHT  = 8
    NIGHT  = 9

    @staticmethod
    def is_valid_digit(digit, card_type=CardType.WAN):
        return Digits.ONE <= digit < CARD_SIZE[card_type]


class Fengs(object):
    DONG = 1
    NAN  = 2
    XI   = 3
    BEI  = 4


class Jians(object):
    ZHONG = 1
    FA    = 2
    BAI   = 3


class HuType(object):
    '''
    胡牌类型
    '''

    # 4×3+2 类
    PI_HU = 1000
    YI_BAN_GAO = 1001           # 1)	一般高：
    LIAN_LIU = 1002             # 2)	连六：
    LAO_SHAO_FU = 1003          # 3)	老少妇：
    YAO_JIU_KE = 1004           # 4)	幺九刻：
    MING_GANG = 1005            # 5)	明杠：
    BIAN_ZHANG = 1006           # 6)	边张：
    KAN_ZHANG = 1007            # 7)	坎张：
    DAN_GOU_JIANG = 1008        # 8)	单钓将：
    ZI_MO = 1009                # 9)	自摸：
    JIAN_KE = 1021                # 1)	箭刻：
    MEN_QIAN_QING = 1022        # 2)	门前清：
    PING_HU = 1023              # 3)	平胡：
    SI_GUI_YI = 1024            # 4)	四归一：
    SHUANG_AN_KE = 1025         # 5)	双暗刻
    AN_GANG = 1026              # 6)	暗杠
    DUAN_YAO = 1027             # 7)	断幺
    BAO_TING = 1028             # 8)	报听：
    QUAN_DAI_YAO = 1041         # 1)	全带幺：
    BU_QIU_REN = 1042           # 2)	不求人：
    SHUANG_MING_GANG = 1043     # 3)	双明杠：
    HU_JUE_ZHANG = 1044         # 4)	胡绝张：
    PENG_PENG_HU = 1061         # 1)	碰碰胡：
    HUN_YI_SE = 1062            # 2)	混一色
    QUAN_QIU_REN = 1063         # 3)	全求人
    SHUANG_JIAN_KE = 1064       # 4)	双箭刻
    MIAO_SHOU_HUI_CHUN = 1081   # 1)	妙手回春
    HAI_DI_LAO_YUE = 1082       # 2)	海底捞月
    GANG_SHANG_KAI_HUA = 1083   # 3)	杠上开花
    QIANG_GANG_HU = 1084        # 4)	抢杠胡
    SHUANG_AN_GANG = 1085       # 5)	双暗杠
    SAN_FENG_KE = 1121          # 1)	三风刻
    QING_LONG = 1161            # 1)	清龙
    YI_SE_SAN_BU_GAO = 1162     # 2)	一色三步高
    SAN_AN_KE = 1163            # 3)	三暗刻
    QING_YI_SE = 1242           # 2)	清一色
    YI_SE_SAN_TONG_SHUN = 1243  # 3)	一色三同顺
    YI_SE_SAN_JIE_GAO = 1244    # 4)	一色三节高
    YI_SE_SI_BU_GAO = 1321      # 1)	一色四步高
    SAN_GANG = 1322             # 2)	三杠
    HUN_YAO_JIU = 1323          # 3)	混幺九
    TIAN_TING = 1324            # 4)	天听
    YI_SE_SI_TONG_SHUN = 1481   # 1)	一色四同顺
    YI_SE_SI_JIE_GAO = 1482     # 2)	一色四节高
    XIAO_SI_XI = 1641           # 1)	小四喜
    XIAO_SAN_YUAN = 1642        # 2)	小三元
    SI_AN_KE = 1643             # 3)	四暗刻
    ZI_YI_SE = 1644             # 4)	字一色
    YI_SE_SHUANG_LONG_HUI = 1645# 5)	一色双龙会
    REN_HU = 1646               # 6)    人胡
    DA_SI_XI = 1881             # 1)	大四喜
    DA_SAN_YUAN = 1882          # 2)	大三元
    JIU_LIAN_BAO_DENG = 1883    # 3)	九莲宝灯
    SI_GANG = 1884              # 4)	四杠
    TIAN_HU = 1886              # 6)	天胡 不记番：边张,坎张,单钓将,不求人,胡绝张,自摸[1006,1007,1008,1042,1044,1009]
    DI_HU = 1887                # 7)	地胡

    # 7×2 类
    QI_XIAO_DUI = 2000          # 1)	七对  胡牌时，牌型由7个对子组成。  不记番：门前清、单钓将、自摸（可算不求人） 。
    QI_LIAN_DUI = 2885          # 5)	七连对 胡牌时，由一种花色序数牌且序数相连的7个对子组成 , 不记番： 清一色、不求人、单钓、门清、七对[1242,1042,1008,1022,2000,2885]

    # 13×1 类
    SHI_SAN_YAO = 3000          # 1)    十三幺

    @classmethod
    def to_dict(cls):
        return {
            "PiHu": cls.PI_HU,
            "YiBanGao": cls.YI_BAN_GAO,
            "LianLiu": cls.LIAN_LIU,
            "LaoShaoFu": cls.LAO_SHAO_FU,
            "YaoJiuKe": cls.YAO_JIU_KE,
            "MingGang": cls.MING_GANG,
            "BianZhang": cls.BIAN_ZHANG,
            "KanZhang": cls.KAN_ZHANG,
            "DanGouJiang": cls.DAN_GOU_JIANG,
            "ZiMo": cls.ZI_MO,
            "JianKe": cls.JIAN_KE,
            "MenQianQing": cls.MEN_QIAN_QING,
            "PingHu": cls.PING_HU,
            "SiGuiYi": cls.SI_GUI_YI,
            "ShuangAnKe": cls.SHUANG_AN_KE,
            "AnGang": cls.AN_GANG,
            "DuanYao": cls.DUAN_YAO,
            "BaoTing": cls.BAO_TING,
            "QuanDaiYao": cls.QUAN_DAI_YAO,
            "BuQiuRen": cls.BU_QIU_REN,
            "ShuangMingGang": cls.SHUANG_MING_GANG,
            "HuJueZhang": cls.HU_JUE_ZHANG,
            "PengPengHu": cls.PENG_PENG_HU,
            "HunYiSe": cls.HUN_YI_SE,
            "QuanQiuRen": cls.QUAN_QIU_REN,
            "ShuangJianKe": cls.SHUANG_JIAN_KE,
            "MiaoShouHuiChun": cls.MIAO_SHOU_HUI_CHUN,
            "HaiDiLaoY": cls.HAI_DI_LAO_YUE,
            "GangShangKaiHua": cls.GANG_SHANG_KAI_HUA,
            "QiangGangHu": cls.QIANG_GANG_HU,
            "ShuangAnGang": cls.SHUANG_AN_GANG,
            "SanFengKe": cls.SAN_FENG_KE,
            "QingLong": cls.QING_LONG,
            "YiSeSanBuGao": cls.YI_SE_SAN_BU_GAO,
            "SanAnKe": cls.SAN_AN_KE,
            "QingYiSe": cls.QING_YI_SE,
            "YiSeSanTongShun": cls.YI_SE_SAN_TONG_SHUN,
            "YiSeSanJieGao": cls.YI_SE_SAN_JIE_GAO,
            "YiSeSiBuGao": cls.YI_SE_SI_BU_GAO,
            "SanGang": cls.SAN_GANG,
            "HunYaoJiu": cls.HUN_YAO_JIU,
            "TianTing": cls.TIAN_TING,
            "YiSeSiTongShun": cls.YI_SE_SI_TONG_SHUN,
            "YiSeSiJieGao": cls.YI_SE_SI_JIE_GAO,
            "XiaoSiXi": cls.XIAO_SI_XI,
            "XiaoSanYuan": cls.XIAO_SAN_YUAN,
            "SiAnKe": cls.SI_AN_KE,
            "ZiYiSe": cls.ZI_YI_SE,
            "YiSeShuangLongHui": cls.YI_SE_SHUANG_LONG_HUI,
            "RenHu": cls.REN_HU,
            "DaSiXi": cls.DA_SI_XI,
            "DaSanYuan": cls.DA_SAN_YUAN,
            "JiuLianBaoDeng": cls.JIU_LIAN_BAO_DENG,
            "SiGang": cls.SI_GANG,
            "TianHu": cls.TIAN_HU,
            "DiHu": cls.DI_HU,
            "QiXiaoDui": cls.QI_XIAO_DUI
        }

    @classmethod
    def get_type(cls, name):
        return cls.to_dict().get(name)
