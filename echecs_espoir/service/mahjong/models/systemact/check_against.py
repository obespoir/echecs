# coding=utf-8

from service.mahjong.constants.gamedefine import Act, CheckAgainType
from service.mahjong.constants.carddefine import LAI_ZI
from service.mahjong.models.systemact.base_system_act import BaseSystemAct
from obespoir.share.ob_log import logger


class CheckAgainst(BaseSystemAct):
    """
    检查其他玩家是否可以操作
    """
    def __init__(self, game_data):
        super(CheckAgainst, self).__init__(game_data=game_data)
        self.check_handler = {
            CheckAgainType.CAN_CHI: self.can_chi,
            CheckAgainType.CAN_PENG: self.can_peng,
            CheckAgainType.CAN_DIAN_GANG: self.can_dian_gang,
            CheckAgainType.CAN_DIAN_PAO: self.can_dian_pao
        }

    def execute(self, cur_seat_id, card_val):
        """
        执行检查
        :param cur_seat_id:
        :param card_val:
        :return:
        """
        logger.debug(u"检查是否有其他玩家可以操作: %s", str([cur_seat_id, card_val]))
        for i in range(self.max_player_num):
            if i == cur_seat_id:
                continue
            self._check(i, card_val)

    def _check(self, seat_id, card_val):
        for check in self.game_config.check_against_check_list:
            self.check_handler.get(check)(seat_id, card_val)

        # 如果玩家可以操作，则添加默认的过操作
        if self.game_data.get_player_can_speaker(seat_id):
            self.game_data.add_player_to_act(seat_id, Act.GUO, act_params={})
        return 1

    def can_chi(self, seat_id, card_val):
        if self.players[seat_id].ting_info:
            # 玩家处于听牌状态，不能吃
            return 0
        if seat_id == self.get_next_seat_id(self.game_data.last_chu_card_seat_id):
            # 只有下家才能吃牌
            chi_result = self.card_analyse.get_can_chi_info_by_handcard(card_val, self.players[seat_id].hand_card)
            if chi_result:
                self.game_data.add_player_to_act(seat_id, Act.CHI, act_params=chi_result)
        return 1

    def can_peng(self, seat_id, card_val):
        if self.players[seat_id].ting_info:
            # 玩家处于听牌状态，不能碰
            return 0
        peng_result = self.card_analyse.get_can_peng_info_by_handcard(card_val, self.players[seat_id].hand_card)
        if peng_result:
            self.game_data.add_player_to_act(seat_id, Act.PENG, act_params={})
        return 1

    def can_dian_gang(self, seat_id, card_val):
        self.players[seat_id].hand_card.add_hand_card_by_vals(card_vals=[card_val])
        gang_result = self.card_analyse.get_can_dian_gang_info_by_handcard(card_val, self.players[seat_id].hand_card)
        self.players[seat_id].hand_card.del_hand_card_by_val(card_val)
        if gang_result:
            if self.players[seat_id].ting_info:
                # 玩家处于听牌状态, 判断点杠后会否破坏牌型
                temp_cards = self.players[seat_id].hand_card.hand_card_vals
                temp_cards.remove(card_val)
                temp_cards.remove(card_val)
                temp_cards.remove(card_val)
                temp_cards.append(LAI_ZI)
                ting_cards = self.card_analyse.get_can_ting_info_by_val(temp_cards)
                ret = []
                for k in ting_cards.keys():
                    ret.extend(ting_cards[k])
                if not set(self.players[seat_id].ting_info.keys()).issubset(set(ret)):
                    # 如果新的听牌结果不包含原有听牌结果，则不能点杠
                    print("seat=%s, card_val=%s, ting_cards=%s , can't ting!" % (seat_id, card_val, ting_cards))
                    return 0

            self.game_data.add_player_to_act(seat_id, Act.DIAN_GANG, act_params={})
        return 1

    def can_dian_pao(self, seat_id, card_val):
        hu_result = self.game_data.hu_manager.check_hu_result(self.players[seat_id].hand_card
                                                              , pao_card_val=self.game_data.last_chu_card_val)
        if hu_result:
            self.game_data.add_player_to_act(seat_id, Act.DIAN_HU, act_params={"hu": hu_result})
        return 1
