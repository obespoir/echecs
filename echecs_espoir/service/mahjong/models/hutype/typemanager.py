# coding=utf-8
import copy

from service.mahjong.constants.carddefine import HuType, BLACK, LAI_ZI
from service.mahjong.models.hutype.eight.gangshangkaihua import GangShangKaiHua
from service.mahjong.models.hutype.eight.haidilaoyue import HaiDiLaoY
from service.mahjong.models.hutype.eight.miaoshouhuichun import MiaoShouHuiChun
from service.mahjong.models.hutype.eight.qiangganghu import QiangGangHu
from service.mahjong.models.hutype.eight.shuangangang import ShuangAnGang
from service.mahjong.models.hutype.eighty_eight.dasanyuan import DaSanYuan
from service.mahjong.models.hutype.eighty_eight.dasixi import DaSiXi
from service.mahjong.models.hutype.eighty_eight.dihu import DiHu
from service.mahjong.models.hutype.eighty_eight.jiulianbaodeng import JiuLianBaoDeng
from service.mahjong.models.hutype.eighty_eight.sigang import SiGang
from service.mahjong.models.hutype.eighty_eight.qiliandui import QiLianDui
from service.mahjong.models.hutype.eighty_eight.tianhu import TianHu
from service.mahjong.models.hutype.forty_eight.yisesijiegao import YiSeSiJieGao
from service.mahjong.models.hutype.forty_eight.yisesitongshun import YiSeSiTongShun
from service.mahjong.models.hutype.four.buqiuren import BuQiuRen
from service.mahjong.models.hutype.four.hujuepai import HuJueZhang
from service.mahjong.models.hutype.four.quandaiyao import QuanDaiYao
from service.mahjong.models.hutype.four.shuangminggang import ShuangMingGang
from service.mahjong.models.hutype.one.bianzhang import BianZhang
from service.mahjong.models.hutype.one.kan_zhang import KanZhang
from service.mahjong.models.hutype.one.dangoujiang import DanGouJiang
from service.mahjong.models.hutype.one.laoshaofu import LaoShaoFu
from service.mahjong.models.hutype.one.yaojiuke import YaoJiuKe
from service.mahjong.models.hutype.one.lianliu import LianLiu
from service.mahjong.models.hutype.one.minggang import MingGang
from service.mahjong.models.hutype.one.yibangao import YiBanGao
from service.mahjong.models.hutype.one.zimo import ZiMo
from service.mahjong.models.hutype.pihu import PiHu
from service.mahjong.models.hutype.qixiaodui import QiXiaoDui
from service.mahjong.models.hutype.shisanyao import ShiSanYao
from service.mahjong.models.hutype.six.hunyise import HunYiSe
from service.mahjong.models.hutype.six.pengpenghu import PengPengHu
from service.mahjong.models.hutype.six.quanqiuren import QuanQiuRen
from service.mahjong.models.hutype.six.shuangjianke import ShuangJianKe
from service.mahjong.models.hutype.sixteen.qinglong import QingLong
from service.mahjong.models.hutype.sixteen.sananke import SanAnKe
from service.mahjong.models.hutype.sixteen.yisesanbugao import YiSeSanBuGao
from service.mahjong.models.hutype.sixty_four.renhu import RenHu
from service.mahjong.models.hutype.sixty_four.sianke import SiAnKe
from service.mahjong.models.hutype.sixty_four.xiaosanyuan import XiaoSanYuan
from service.mahjong.models.hutype.sixty_four.xiaosixi import XiaoSiXi
from service.mahjong.models.hutype.sixty_four.yiseshuanglonghui import YiSeShuangLongHui
from service.mahjong.models.hutype.sixty_four.ziyise import ZiYiSe
from service.mahjong.models.hutype.thirty_two.hunyaojiu import HunYaoJiu
from service.mahjong.models.hutype.thirty_two.sangang import SanGang
from service.mahjong.models.hutype.thirty_two.tianting import TianTing
from service.mahjong.models.hutype.thirty_two.yisesibugao import YiSeSiBuGao
from service.mahjong.models.hutype.twelve.sanfengke import SanFengKe
from service.mahjong.models.hutype.twenty_four.qingyise import QingYiSe
from service.mahjong.models.hutype.twenty_four.yisesanjiegao import YiSeSanJieGao
from service.mahjong.models.hutype.twenty_four.yisesantongshun import YiSeSanTongShun
from service.mahjong.models.hutype.two.angang import AnGang
from service.mahjong.models.hutype.two.baoting import BaoTing
from service.mahjong.models.hutype.two.duanyao import DuanYao
from service.mahjong.models.hutype.two.jianke import JianKe
from service.mahjong.models.hutype.two.menqianqing import MenQianQing
from service.mahjong.models.hutype.two.pinghu import PingHu
from service.mahjong.models.hutype.two.shuanganke import ShuangAnKe
from service.mahjong.models.hutype.two.siguiyi import SiGuiYi

"""
番型管理器:
添加番型方法  1:在 hutype 中建立番型文件, 并编写番型类及其计算方法
            2:在 HU_TYPE_DICT, 添加对应Key
            3:如果要使用此番型判定,需要在 game_setting->default.json->used_hu_types, hu_fan_info中配置此游戏使用的番型
            4:需要在 game_setting->hu_fan_info 设置各牌型番数
            5:carddefine.py中,HuType添加响应类型,  to_dict 中添加响应配型解析key 需要和default.json中配置一一对应

"""

# 胡牌胡法对象
HU_TYPE_DICT = {
    HuType.PI_HU: PiHu(),
    HuType.YI_BAN_GAO: YiBanGao(),
    HuType.LIAN_LIU: LianLiu(),
    HuType.LAO_SHAO_FU: LaoShaoFu(),
    HuType.YAO_JIU_KE: YaoJiuKe(),
    HuType.MING_GANG: MingGang(),
    HuType.BIAN_ZHANG: BianZhang(),                 # 6)	边张：
    HuType.KAN_ZHANG: KanZhang(),                         # 7)	坎张：
    HuType.DAN_GOU_JIANG: DanGouJiang(),            # 8)	单钓将：
    HuType.ZI_MO: ZiMo(),                           # 9)	自摸：
    HuType.JIAN_KE: JianKe(),                       # 1)	箭刻：
    HuType.MEN_QIAN_QING: MenQianQing(),            # 2)	门前清：
    HuType.PING_HU: PingHu(),                       # 3)	平胡：
    HuType.SI_GUI_YI: SiGuiYi(),                    # 4)	四归一：
    HuType.SHUANG_AN_KE: ShuangAnKe(),              # 5)	双暗刻
    HuType.AN_GANG: AnGang(),                       # 6)	暗杠
    HuType.DUAN_YAO: DuanYao(),                     # 7)	断幺
    HuType.BAO_TING: BaoTing(),                     # 8)	报听：
    HuType.QUAN_DAI_YAO: QuanDaiYao(),              # 1)	全带幺：
    HuType.BU_QIU_REN: BuQiuRen(),                  # 2)	不求人：
    HuType.SHUANG_MING_GANG: ShuangMingGang(),      # 3)	双明杠：
    HuType.HU_JUE_ZHANG: HuJueZhang(),              # 4)	胡绝张：
    HuType.PENG_PENG_HU: PengPengHu(),              # 1)	碰碰胡：
    HuType.HUN_YI_SE: HunYiSe(),                    # 2)	混一色
    HuType.QUAN_QIU_REN: QuanQiuRen(),              # 3)	全求人
    HuType.SHUANG_JIAN_KE: ShuangJianKe(),          # 4)	双箭刻
    HuType.MIAO_SHOU_HUI_CHUN: MiaoShouHuiChun(),   # 1)	妙手回春
    HuType.HAI_DI_LAO_YUE: HaiDiLaoY(),             # 2)	海底捞月
    HuType.GANG_SHANG_KAI_HUA: GangShangKaiHua(),   # 3)	杠上开花
    HuType.QIANG_GANG_HU: QiangGangHu(),            # 4)	抢杠胡
    HuType.SHUANG_AN_GANG: ShuangAnGang(),          # 5)	双暗杠
    HuType.SAN_FENG_KE: SanFengKe(),                # 1)	三风刻
    HuType.QING_LONG: QingLong(),                   # 1)	清龙
    HuType.YI_SE_SAN_BU_GAO: YiSeSanBuGao(),        # 2)	一色三步高
    HuType.SAN_AN_KE: SanAnKe(),                    # 3)	三暗刻
    HuType.QING_YI_SE: QingYiSe(),                  # 2)	清一色
    HuType.YI_SE_SAN_TONG_SHUN: YiSeSanTongShun(),  # 3)	一色三同顺
    HuType.YI_SE_SAN_JIE_GAO: YiSeSanJieGao(),      # 4)	一色三节高
    HuType.YI_SE_SI_BU_GAO: YiSeSiBuGao(),          # 1)	一色四步高
    HuType.SAN_GANG: SanGang(),                     # 2)	三杠
    HuType.HUN_YAO_JIU: HunYaoJiu(),                # 3)	混幺九
    HuType.TIAN_TING: TianTing(),                   # 4)	天听
    HuType.YI_SE_SI_TONG_SHUN: YiSeSiTongShun(),    # 1)	一色四同顺
    HuType.YI_SE_SI_JIE_GAO: YiSeSiJieGao(),        # 2)	一色四节高
    HuType.XIAO_SI_XI: XiaoSiXi(),                  # 1)	小四喜
    HuType.XIAO_SAN_YUAN: XiaoSanYuan(),            # 2)	小三元
    HuType.SI_AN_KE: SiAnKe(),                      # 3)	四暗刻
    HuType.ZI_YI_SE: ZiYiSe(),                      # 4)	字一色
    HuType.YI_SE_SHUANG_LONG_HUI: YiSeShuangLongHui(),  # 5)	一色双龙会
    HuType.REN_HU: RenHu(),                         # 6)    人胡
    HuType.DA_SI_XI: DaSiXi(),                      # 1)	大四喜
    HuType.DA_SAN_YUAN: DaSanYuan(),                # 2)	大三元
    HuType.JIU_LIAN_BAO_DENG: JiuLianBaoDeng(),     # 3)	九莲宝灯
    HuType.SI_GANG: SiGang(),                       # 4)	四杠
    HuType.QI_LIAN_DUI: QiLianDui(),                # 5)	七连对
    HuType.TIAN_HU: TianHu(),                       # 6)	天胡
    HuType.DI_HU: DiHu(),                           # 7)	地胡


    HuType.QI_XIAO_DUI: QiXiaoDui(),

    HuType.SHI_SAN_YAO: ShiSanYao()
}


class HuTypeManager(object):
    """
    胡牌类型管理
    """

    def __init__(self, game_config, card_analyse):
        super(HuTypeManager, self).__init__()

        self.card_analyse = card_analyse
        self.fan_info = game_config.hu_fan_info
        self.mutex_list = game_config.mutex_list
        self.type_info = game_config.used_hu_types  # 特殊胡牌牌型信息, key存放基础胡牌类型， value存放特殊胡牌类型
        print("used_hu_types = ", game_config.used_hu_types)
        # {HuType.PI_HU: [HuType.PENG_PENG_HU, ...],HuType.QI_XIAO_DUI: []}
        self.base_hu_types = self.type_info.keys()
        self.special_hu_types = []

    def get_special_types(self, base_types=[]):
        """
        获取需要判断的特殊胡法类型
        :param base_types: 基础胡法类型[1000,2000]
        :return:
        """
        special_types = []
        for bt in base_types:
            for st in self.type_info.get(bt, []):
                if st not in special_types:
                    special_types.append(st)

        return special_types

    def check_ting_result(self, hand_card):
        """
        检查是否可以听牌
        :param hand_card:
        :return: {出牌１：{胡的牌:{"fan":胡牌基本类型番数, "type_list":[胡牌类型]}, ...}
        """
        if 2 != len(hand_card.hand_card_vals) % 3:
            return {}
        # 组合联合手牌
        hand_card.union_hand_card()
        ret = {}
        temp_card_vals = list(set(hand_card.hand_card_vals))
        for c in temp_card_vals:
            cards = hand_card.hand_card_vals
            cards.append(LAI_ZI)
            cards.remove(c)
            ting_infos = self.card_analyse.get_can_ting_info_by_val(cards)
            if ting_infos:
                ret[c] = {}
                hand_card.del_hand_card_by_val(c)
                for bt, lst in ting_infos.items():
                    for tc in lst:
                        hand_card.add_hand_card_by_vals(card_vals=[tc])
                        special_hu_list = self.check_special_hu(hand_card, [bt])
                        print("special_hu_list = ", special_hu_list)
                        can_hu_list = copy.deepcopy(special_hu_list)
                        can_hu_list.append(bt)
                        print("can_hu_list = ", can_hu_list)
                        mutexed_list = self.remove_mutex_type(can_hu_list)
                        print("mutexed_list = ", mutexed_list)
                        total_fan = self.get_fan_hu_type_list(mutexed_list)
                        ret[c][tc] = {"fan": total_fan, "type_list": mutexed_list}
                        hand_card.del_hand_card_by_val(tc)
                hand_card.add_hand_card_by_vals(card_vals=[c])
        return ret

    def check_hu_result(self, hand_card, pao_card_val=BLACK):
        """
        检查胡牌结果
        :param hand_card: 待检查的手牌信息, 手牌对象
        :param pao_card_val: 点炮的牌
        :return: 返回可胡牌类型
        """
        if pao_card_val:
            hand_card.add_hand_card_by_vals(card_vals=[pao_card_val])
        base_type_list = self.check_base_hu(hand_card)
        can_hu_type_list = copy.deepcopy(base_type_list)
        if base_type_list:
            special_type_list = self.check_special_hu(hand_card, base_type_list)
            can_hu_type_list.extend(special_type_list)
        if pao_card_val:
            hand_card.del_hand_card_by_val(pao_card_val)
        # 去除互斥胡法
        return self.remove_mutex_type(can_hu_type_list)

    def check_base_hu(self, hand_card):
        """
        检查是否可胡基本牌型
        :param hand_card: hand_card 对象，手牌数要求为 %3=2张
        return: base_type_list: []
        """
        base_type_list = []
        for i in self.base_hu_types:
            if HU_TYPE_DICT.get(i).is_this_type(hand_card, self.card_analyse):
                base_type_list.append(i)
        return base_type_list

    def check_special_hu(self, hand_card, base_type_list):
        """
        检查是否可胡特殊牌型
        :param hand_card: hand_card 对象，手牌数要求为 %3=2张
        return: base_type_list: []
        """
        special_type_list = []
        need_judge_types = self.get_special_types(base_type_list)
        for st in need_judge_types:
            if HU_TYPE_DICT.get(st).is_this_type(hand_card, self.card_analyse, ):
                special_type_list.append(st)
        return special_type_list

    def remove_mutex_type(self, type_list):
        """
        处理互斥牌型
        :param type_list:
        :return: [] 胡牌所包含的牌型
        """
        if HuType.PI_HU in type_list and 1 < len(type_list):
            # 默认只要存在其他胡法，屁胡则不计算进入胡牌类型
            type_list.remove(HuType.PI_HU)

        # logger.debug(u"[%s,uid=%s,did=%s,cid=%s] %s" % (func_name, userid, deskid, commandid, params))

        # 互斥胡法中只选择番数最高的
        for lst in self.mutex_list:
            if lst:
                tmp = list(set(lst) & set(type_list))
                if tmp:
                    max_type = tmp[0]
                    for i in tmp:
                        if self.fan_info[i] > self.fan_info[max_type]:
                            max_type = tmp[1]
                    type_list = list(set(type_list) - set(lst))
                    type_list.append(max_type)
        return type_list

    def get_fan_hu_type_list(self, type_list=[]):
        """
        获取指定类型列表的番数, 番数累加
        :param type_list:
        :return: 返回总番数
        """
        sum_fan = 0
        for t in type_list:
            if not self.fan_info.get(t):
                print("fan_info=", self.fan_info)
                raise Exception("t=%s" % t)
            sum_fan += self.fan_info.get(t)
        return sum_fan
