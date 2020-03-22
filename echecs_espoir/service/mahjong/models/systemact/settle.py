# coding=utf-8

from share import message_ids
from service.mahjong.constants.gamedefine import Act, SettleType, GangType, HuSettleParamType, SettleHuFan
from service.mahjong.controls.notifybridge import notify_settle_data
from service.mahjong.models.systemact.base_system_act import BaseSystemAct
from obespoir.share.ob_log import logger


class Settle(BaseSystemAct):
    """
    游戏结算
    """
    def __init__(self, game_data):
        super(Settle, self).__init__(game_data=game_data)
        self.settle_hu_handler = {
            SettleHuFan.ZHUANG: self.get_extra_fan_zhuang,
            SettleHuFan.DIAN_GANG: self.get_extra_fan_dian_gang,
            SettleHuFan.BU_GANG: self.get_extra_fan_bu_gang,
            SettleHuFan.AN_GANG: self.get_extra_fan_an_gang,
            SettleHuFan.HUA: self.get_extra_fan_hua,
            SettleHuFan.JIA_MA: self.get_extra_fan_jia_ma,
            SettleHuFan.JIA_PIAO: self.get_extra_fan_jia_piao,
            SettleHuFan.LIANG_DAO: self.get_extra_fan_liang_dao,
            SettleHuFan.GUO_HU: self.get_extra_fan_guo_hu,
            SettleHuFan.GANG_SHANG_PAO: self.get_extra_fan_gang_shang_pao,
            SettleHuFan.GANG_SHANG_KAI_HUA: self.get_extra_fan_gang_shang_kai_hua,
            SettleHuFan.QIANG_BU_GANG_HU: self.get_extra_fan_qiang_bu_gang_hu
        }

    def execute(self, type_list=[SettleType.HU]):
        """
        执行结算
        :param params:  {settletype:[], settletype2:[,...], ...}
        :return:
        """
        logger.debug(u"执行结算: %s", str(type_list))
        for i in range(self.game_data.max_player_num):
            self.players[i].hand_card.handle_hand_card_for_settle_show()
            # 联合手牌,用于计算胡牌番型
            self.game_data.players[i].hand_card.union_hand_card()

        for t in type_list:
            if SettleType.GANG == t:
                self.settle_gang()
            elif SettleType.GEN_ZHUANG == t:
                self.settle_gen_zhuang()
            elif SettleType.HU == t:
                self.settle_hu()
            elif SettleType.DRAW == t:
                self.settle_draw()

        # 返回结算数据
        notify_settle_data(self.desk_id, self.game_data.settle_data)

    def settle_gang(self):
        for i in range(self.max_player_num):
            for val in self.players[i].hand_card.dian_gang_card_vals:
                tmp_points = [0 for j in range(self.max_player_num)]
                gang_fan = self.game_config.settle_gang_info.get(Act.DIAN_GANG)
                tmp_points[i] = gang_fan
                source = self.players[i].hand_card.dian_gang_source.get(val)
                tmp_points[source] = -gang_fan
                self.game_data.add_settle_info(self, SettleType.GANG, seat_points=tmp_points,
                                               params={"type": GangType.DIAN_GANG, "source": source})
            for _ in self.players[i].hand_card.bu_gang_card_vals:
                gang_fan = self.game_config.settle_gang_info.get(Act.BU_GANG)
                tmp_points = [-gang_fan for _ in range(self.max_player_num)]
                tmp_points[i] = gang_fan * (self.max_player_num-1)
                self.game_data.add_settle_info(self, SettleType.GANG, seat_points=tmp_points,
                                               params={"type": GangType.BU_GANG})
            for _ in self.players[i].hand_card.an_gang_card_vals:
                gang_fan = self.game_config.settle_gang_info.get(Act.AN_GANG)
                tmp_points = [-gang_fan for j in range(self.max_player_num)]
                tmp_points[i] = gang_fan * (self.max_player_num-1)
                self.game_data.add_settle_info(self, SettleType.GANG, seat_points=tmp_points,
                                               params={"type": GangType.AN_GANG})

    def settle_gen_zhuang(self):
        pass

    def settle_hu(self):
        """
        胡牌结算
        某玩家胡牌的计算公式为：
        y = (A(x+B)+C) * D
        y 为 胡牌最终番数， X为基本胡法番数， 如碰碰胡清一色共4番，x=4
        A = A1*A2*..., A为算最终番数相乘的因子积
        B = B1+B2+..., B为算番时和基础番数相加的因子和
        C = C1+C2+..., C为算最终番时相加的因子积
        :return:
        """
        for seat_id, params in self.game_data.hu_player_static.items():
            base_fan = self.game_data.hu_manager.get_fan_hu_type_list(params.get("type_list"))
            tmp_points = self.compute_tpm_fan(base_fan, seat_id,
                                              self.players[seat_id].hand_card.guo_hu_num,
                                              self.game_config.base_bet)
            hand_card_for_settle_show = self.game_data.players[seat_id].hand_card.hand_card_for_settle_show
            self.game_data.add_settle_info(
                SettleType.HU,
                seat_points=tmp_points,
                params={"type_list": params.get("type_list"),
                        "hu_seat_id": seat_id,
                        "hu_fan_count": base_fan,
                        "guo_hu_count": self.game_data.players[seat_id].hand_card.guo_hu_num,
                        "source_seat_id": params.get('source_seat_id', -1),
                        "hand_card_for_settle_show": hand_card_for_settle_show
                        }
            )


    def settle_draw(self):
        """
        荒牌结算
        """
        tmp_points = [0 for _ in range(self.max_player_num)]
        self.game_data.add_settle_info(SettleType.DRAW, seat_points=tmp_points, params={"hu_seat_id": -1})

    def compute_tpm_fan(self, base_fan, hu_seat_id, guo_hu_count=0, base_bet=1):
        """
        计算二人麻将胡牌后点数输赢
        :param base_fan: 番数
        :param hu_seat_id: 胡牌玩家位置
        :param guo_hu_count: 过户次数
        :param base_bet: 本场次底分
        :return:
        """
        points = [0 for _ in range(self.max_player_num)]
        for i in range(self.max_player_num):
            last_fan = self.get_settle_hu_fan(base_fan, hu_seat_id, i)
            if hu_seat_id == i:
                points[i] = last_fan * base_bet * pow(2, guo_hu_count)
            else:
                points[i] = -last_fan * base_bet * pow(2, guo_hu_count)
        return points


    def compute_last_fan(self, base_fan, hu_seat_id, is_zi_mo=0, source=-1):
        """
        进行结成后的最终番数
        某玩家胡牌的计算公式为：
        y = (A(x+B)+C) * D
        y 为 胡牌最终番数， X为基本胡法番数， 如碰碰胡清一色共4番，x=4
        A = A1*A2*..., A为算最终番数相乘的因子积
        B = B1+B2+..., B为算番时和基础番数相加的因子和
        C = C1+C2+..., C为算最终番时相加的因子积
        :param base_fan:
        :param hu_seat_id:
        :param is_zi_mo:
        :param source:
        :return: [...]
        """
        points = [0 for _ in range(self.max_player_num)]
        win_fan = 0
        if is_zi_mo:
            for i in range(self.max_player_num):
                if hu_seat_id == i:
                    continue
                last_fan = self.get_settle_hu_fan(base_fan, hu_seat_id, i)
                win_fan += win_fan
                points[i] = -last_fan
        else:
            last_fan = self.get_settle_hu_fan(base_fan, hu_seat_id, source)
            points[source] = -last_fan
            win_fan = last_fan

        points[hu_seat_id] = win_fan
        return points

    def get_settle_hu_fan(self, base_fan, hu_seat_id, seat_id):
        a = self.compute_fan_A(hu_seat_id, seat_id)
        b = self.compute_fan_B(hu_seat_id, seat_id)
        c = self.compute_fan_C(hu_seat_id, seat_id)
        d = self.compute_fan_D(hu_seat_id, seat_id)
        return (a * (base_fan + b) + c) * d

    def compute_fan_A(self, hu_seat_id, seat_id):
        fan = 1
        for t in self.game_config.settle_fan_config.get(HuSettleParamType.A).keys():
            fan = fan * self.settle_hu_handler.get(t)(hu_seat_id, seat_id, p_type=HuSettleParamType.A)
        return fan

    def compute_fan_B(self, hu_seat_id, seat_id):
        fan = 0
        for t in self.game_config.settle_fan_config.get(HuSettleParamType.B).keys():
            fan = fan + self.settle_hu_handler.get(t)(hu_seat_id, seat_id, p_type=HuSettleParamType.B)
        return fan

    def compute_fan_C(self, hu_seat_id, seat_id):
        fan = 0
        for t in self.game_config.settle_fan_config.get(HuSettleParamType.C).keys():
            fan = fan + self.settle_hu_handler.get(t)(hu_seat_id, seat_id, p_type=HuSettleParamType.C)
        return fan

    def compute_fan_D(self, hu_seat_id, seat_id):
        fan = 1
        for t in self.game_config.settle_fan_config.get(HuSettleParamType.D).keys():
            fan = fan * self.settle_hu_handler.get(t)(hu_seat_id, seat_id, p_type=HuSettleParamType.D)
        return fan

    def get_extra_fan_zhuang(self, hu_seat_id, seat_id, p_type = HuSettleParamType.A):
        has_zhuang_rel = 0
        base_ratio = 1 if p_type in [HuSettleParamType.A, HuSettleParamType.D] else 0
        if seat_id == self.game_data.banker_seat_id or hu_seat_id==self.game_data.banker_seat_id:
            has_zhuang_rel = 1
        if has_zhuang_rel:
            return self.game_config.settle_fan_config.get(p_type).get(SettleHuFan.ZHUANG)
        return base_ratio

    def get_extra_fan_dian_gang(self, hu_seat_id, seat_id, p_type=HuSettleParamType.A):
        base_ratio = 1 if p_type in [HuSettleParamType.A, HuSettleParamType.D] else 0
        if hu_seat_id == seat_id:
            return base_ratio
        dian_gang_num = 0
        for c, s in self.players[hu_seat_id].hand_card.dian_gang_source.items():
            if s == seat_id:
                dian_gang_num += 1
        if 0 == dian_gang_num:
            return base_ratio

        return dian_gang_num * self.game_config.settle_fan_config.get(p_type).get(SettleHuFan.DIAN_GANG)

    def get_extra_fan_bu_gang(self, hu_seat_id, seat_id, p_type=HuSettleParamType.A):
        base_ratio = 1 if p_type in [HuSettleParamType.A, HuSettleParamType.D] else 0
        bu_gang_num = len(self.players[seat_id].hand_card.bu_gang_card_vals)
        if 0 == bu_gang_num:
            return base_ratio

        return bu_gang_num * self.game_config.settle_fan_config.get(p_type).get(SettleHuFan.BU_GANG)

    def get_extra_fan_an_gang(self, hu_seat_id, seat_id, p_type=HuSettleParamType.A):
        base_ratio = 1 if p_type in [HuSettleParamType.A, HuSettleParamType.D] else 0
        an_gang_num = len(self.players[seat_id].hand_card.an_gang_card_vals)
        if 0 == an_gang_num:
            return base_ratio

        return an_gang_num * self.game_config.settle_fan_config.get(p_type).get(SettleHuFan.AN_GANG)

    def get_extra_fan_jia_ma(self, hu_seat_id, seat_id, p_type=HuSettleParamType.A):
        #TOdo
        base_ratio = 1 if p_type in [HuSettleParamType.A, HuSettleParamType.D] else 0
        return base_ratio

    def get_extra_fan_jia_piao(self, hu_seat_id, seat_id, p_type=HuSettleParamType.A):
        #TOdo
        base_ratio = 1 if p_type in [HuSettleParamType.A, HuSettleParamType.D] else 0
        return base_ratio

    def get_extra_fan_hua(self, hu_seat_id, seat_id, p_type=HuSettleParamType.A):
        #TOdo
        base_ratio = 1 if p_type in [HuSettleParamType.A, HuSettleParamType.D] else 0
        return base_ratio

    def get_extra_fan_liang_dao(self, hu_seat_id, seat_id, p_type=HuSettleParamType.A):
        #TOdo
        base_ratio = 1 if p_type in [HuSettleParamType.A, HuSettleParamType.D] else 0
        return base_ratio

    def get_extra_fan_guo_hu(self, hu_seat_id, seat_id, p_type=HuSettleParamType.A):
        #TOdo
        base_ratio = 1 if p_type in [HuSettleParamType.A, HuSettleParamType.D] else 0
        return base_ratio

    def get_extra_fan_gang_shang_pao(self, hu_seat_id, seat_id, p_type=HuSettleParamType.A):
        base_ratio = 1 if p_type in [HuSettleParamType.A, HuSettleParamType.D] else 0
        record = self.game_data.act_record_list[-2]
        if record.act_type in [Act.BU_GANG, Act.DIAN_GANG, Act.AN_GANG] and record.seat_id != hu_seat_id:
            # 倒数第一个动作为出牌，第二个为杠　
            return self.game_config.settle_fan_config.get(p_type).get(SettleHuFan.GANG_SHANG_PAO)
        return base_ratio

    def get_extra_fan_gang_shang_kai_hua(self, hu_seat_id, seat_id, p_type=HuSettleParamType.A):
        base_ratio = 1 if p_type in [HuSettleParamType.A, HuSettleParamType.D] else 0
        record = self.game_data.act_record_list[-1]
        if record.act_type in [Act.BU_GANG, Act.DIAN_GANG, Act.AN_GANG] and record.seat_id == hu_seat_id:
            # 倒数第一个动作为杠　
            return self.game_config.settle_fan_config.get(p_type).get(SettleHuFan.GANG_SHANG_PAO)
        return base_ratio

    def get_extra_fan_qiang_bu_gang_hu(self, hu_seat_id, seat_id, p_type=HuSettleParamType.A):
        # 抢补杠胡
        base_ratio = 1 if p_type in [HuSettleParamType.A, HuSettleParamType.D] else 0
        if self.players[hu_seat_id].hook_hu_seat_id == seat_id:
            self.players[hu_seat_id].reset_hook()
            return self.game_config.settle_fan_config.get(p_type).get(SettleHuFan.QIANG_BU_GANG_HU)
        return base_ratio
