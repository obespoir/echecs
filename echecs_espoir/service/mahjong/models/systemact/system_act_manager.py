# coding=utf-8

from service.mahjong.constants.gamedefine import SystemActType
from service.mahjong.controls.gamemanager import game_manager
from obespoir.share.ob_log import logger


class SystemActManager(object):
    """
    系统动作管理类
    """
    instances = {}

    def __init__(self, game_data):
        self.acts = {}
        self.game_data = game_data
        self.handler = {
            SystemActType.GEN_BANK: self.gen_bank,
            SystemActType.DEAL_CARD: self.deal_card,
            SystemActType.DRAW_CARD: self.draw_card,
            SystemActType.CHECK_AGAINST: self.check_against,
            SystemActType.SETTLE: self.settle,
            SystemActType.GAME_OVER: self.game_over
        }

    @classmethod
    def get_instance(cls, desk_id):
        if desk_id not in cls.instances.keys():
            game_desk = game_manager.get_game_desk(desk_id)
            cls.instances[desk_id] = SystemActManager(game_desk.game_data)
        return cls.instances[desk_id]

    def try_settle_hu(self, hu_seat_id, is_zi_mo, hu_type_list, source=-1, hook_seat_id=-1):
        '''
        计算可能的胡牌结算番数
        :param hu_type_list: 胡牌的类型
        :param virtual_params: 虚拟未发生的操作参数，用来计算可能出现的胡牌番型
        :return:
        '''
        from service.mahjong.models.systemact.settle import Settle
        if not self.acts.get("settle", None):
            self.acts['settle'] = Settle(game_data=self.game_data)
        old_hook_seat_id = self.game_data.players[hu_seat_id].hook_hu_seat_id
        self.game_data.players[hu_seat_id].hook_hu_seat_id = hook_seat_id
        base_fan = self.game_data.hu_manager.get_fan_hu_type_list(hu_type_list)
        tmp_points = self.acts['settle'].compute_last_fan(base_fan, hu_seat_id, is_zi_mo=is_zi_mo,
                                                          source=source)
        self.game_data.players[hu_seat_id].hook_hu_seat_id = old_hook_seat_id
        return max(tmp_points)

    def system_act(self, act_type, act_params={}):
        print("system_act act_params=", act_params)
        if act_type not in self.handler.keys():
            logger.debug(u"system_act param error:%s", str([act_type, act_params]))
            return
        return self.handler.get(act_type)(act_params)

    def gen_bank(self, act_params):
        from service.mahjong.models.systemact.gen_bank import GenBank
        if not self.acts.get("gen_bank", None):
            self.acts['gen_bank'] = GenBank(game_data=self.game_data)
        return self.acts["gen_bank"].execute()

    def deal_card(self, act_params):
        from service.mahjong.models.systemact.deal_card import DealCard
        if not self.acts.get("deal_card", None):
            self.acts['deal_card'] = DealCard(game_data=self.game_data)
        return self.acts["deal_card"].execute()

    def draw_card(self, act_params):
        from service.mahjong.models.systemact.draw_card import DrawCard
        if not self.acts.get("draw_card", None):
            self.acts['draw_card'] = DrawCard(game_data=self.game_data)
        seat_id = act_params.get('seat_id', self.game_data.banker_seat_id)
        card_num = act_params.get("card_num", 1)
        is_last = act_params.get("is_last", False)
        return self.acts["draw_card"].execute(seat_id, card_num, is_last)

    def check_against(self, act_params):
        from service.mahjong.models.systemact.check_against import CheckAgainst
        if not self.acts.get("check_against", None):
            self.acts['check_against'] = CheckAgainst(game_data=self.game_data)
        cur_seat_id = act_params.get('cur_seat_id')
        card = act_params.get("card")
        return self.acts["check_against"].execute(cur_seat_id, card)

    def settle(self, act_params):
        from service.mahjong.models.systemact.settle import Settle
        if not self.acts.get("settle", None):
            self.acts['settle'] = Settle(game_data=self.game_data)
        type_list = act_params.get('type_list', [])
        return self.acts["settle"].execute(type_list)

    def game_over(self, act_params):
        from service.mahjong.models.systemact.game_over import GameOver
        if not self.acts.get("game_over", None):
            self.acts['game_over'] = GameOver(game_data=self.game_data)
        return self.acts["game_over"].execute()