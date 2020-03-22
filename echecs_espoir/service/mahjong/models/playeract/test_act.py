# coding=utf-8

__author__ = 'jamon'

from config.globalconfig import GlobalConfig
from obespoir.share.ob_log import logger
from share.message_ids import USER_TEST_ACT
from share.errorcode import CARD_NOT_IN_HAND_CARD, TEST_PARAMS_ERROR, CANT_USE_TEST, CANT_USE_TEST_GAME_STATUS_UN_AGREE, NEED_S_CARD_T_CARD
from service.mahjong.constants.gamedefine import Act, TestActionType
from service.mahjong.controls.notifybridge import notify_single_user
from service.mahjong.constants.gamedefine import GameStatus
from service.mahjong.models.playeract.base_player_act import BasePlayerAct


class TestAct(BasePlayerAct):
    """測試接口"""
    def __init__(self, game_data):
        super(TestAct, self).__init__(game_data=game_data)
        self.game_data = game_data
        self.handlers = {
            TestActionType.HUAN_CARD: self.huan_card,                       # 換牌
            TestActionType.SURE_NEXT_CARDS: self.sure_next_cards,           # 确定接下来的牌
            TestActionType.GET_LAST_CARD: self.get_last_card,               # 胡碰碰胡
            TestActionType.INIT_DRAW_CARDS: self.init_draw_cards,           # 初始化发牌
            TestActionType.QUICK_DRAW: self.quick_draw                      # 快速留局
        }

    def execute(self, seat_id, act, card_list):
        """
        执行测试换牌
        :param act_params:
        :return:
        """
        logger.debug(u"測試换牌: %s", str([seat_id, act, card_list]))
        return self.handlers.get(act)(seat_id, card_list)

    def huan_card(self, seat_id, test_params):
        if not self.game_data.game_config.test_mode:
            self.notify_player_card_change(seat_id, code=CANT_USE_TEST)
            return
        logger.debug(u"换牌：%s", str([seat_id, test_params]))
        old_card = test_params.get("source_card")[0]
        new_card = test_params.get("target_card")[0]
        if not old_card or not new_card:
            self.notify_player_card_change(seat_id, code=NEED_S_CARD_T_CARD)
            return
        if not self.players[seat_id].hand_card.has_card(old_card):
            self.notify_player_card_change(seat_id, code=CARD_NOT_IN_HAND_CARD)
            return
        self.players[seat_id].hand_card.del_hand_card_by_val(card_val=old_card)
        self.players[seat_id].hand_card.add_hand_card_by_vals(card_vals=[new_card])
        self.notify_player_card_change(seat_id)

    def sure_next_cards(self, seat_id, test_params):
        if not self.game_data.game_config.test_mode:
            self.notify_player_card_change(seat_id, code=CANT_USE_TEST)
            return
        card_list = test_params.get("target_card")
        if not isinstance(card_list, list):
            self.notify_player_card_change(seat_id, TEST_PARAMS_ERROR)
            return
        logger.debug(u"确定接下来的牌：%s", str([seat_id, card_list]))
        if GlobalConfig().test_sure_next_cards.get(self.desk_id):
            GlobalConfig().test_sure_next_cards[self.desk_id][seat_id].extend(card_list)
        else:
            GlobalConfig().test_sure_next_cards[self.desk_id] = [[] for _ in range(self.game_data.max_player_num)]
            GlobalConfig().test_sure_next_cards[self.desk_id][seat_id].extend(card_list)

        self.notify_player_next(seat_id)



    def get_last_card(self, seat_id, card_list):
        if not self.game_data.game_config.test_mode:
            self.notify_player_card_change(seat_id, code=CANT_USE_TEST)
            return
        logger.debug(u"获取最后一张牌：%s", str([seat_id, card_list]))
        last_card = self.game_data.card_dealer.get_the_last_card()
        self.notify_player(seat_id, [last_card])

    def init_draw_cards(self, seat_id, test_params):

        self.notify_player_card_change(seat_id, code=CANT_USE_TEST_GAME_STATUS_UN_AGREE)


    def quick_draw(self, seat_id, test_params):
        if not self.game_data.game_config.test_mode:
            self.notify_player_card_change(seat_id, code=CANT_USE_TEST)
            return
        self.game_data.card_dealer.card_count = 0
        self.notify_player_quick_draw(seat_id)


    def notify_player_card_change(self, seat_id, code=200):
        data = {"test_type": TestActionType.HUAN_CARD,
                "seat_id": seat_id,
                "hand_card": self.players[seat_id].hand_card.hand_card_vals}
        notify_single_user(self.desk_id, seat_id, USER_TEST_ACT, data, code)

    def notify_player_next(self, seat_id, code=200):
        data = {"test_type": TestActionType.SURE_NEXT_CARDS,
                "seat_id": seat_id,
                "next_cards": GlobalConfig().test_sure_next_cards[self.desk_id][seat_id]}
        notify_single_user(self.desk_id, seat_id, USER_TEST_ACT, data, code)

    def notify_player(self, seat_id, cards, code=200):
        data = {"test_type": TestActionType.GET_LAST_CARD, "seat_id": seat_id, "cards": cards}
        notify_single_user(self.desk_id, seat_id, USER_TEST_ACT, data, code)

    def notify_player_quick_draw(self, seat_id, code=200):
        data = {"test_type": TestActionType.QUICK_DRAW, "seat_id": seat_id, "remain_cards": 0}
        notify_single_user(self.desk_id, seat_id, USER_TEST_ACT, data, code)
