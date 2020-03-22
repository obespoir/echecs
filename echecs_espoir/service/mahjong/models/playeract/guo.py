# coding=utf-8

__author__ = 'jamon'

from obespoir.share.ob_log import logger
from share.message_ids import *
from service.mahjong.models.playeract.base_player_act import BasePlayerAct
from service.mahjong.constants.gamedefine import Act, GameActStatus, SystemActType
from service.mahjong.models.actrecord import ActRecord
from service.mahjong.models.callbackmanager import CallbackFuncType, CallbackManager


class Guo(BasePlayerAct):
    def __init__(self, game_data):
        super(Guo, self).__init__(game_data=game_data)
        self.step_handlers = {
            "param_check": self.param_check,  # 参数验证
            "set_data": self.set_data,  # 参数验证
            "next_act": self.next_act         # 通知桌子进行下一步操作
        }

        self.seat_id = -1  # 执行出牌的玩家位置

    def execute(self, act_params={}):
        """
        执行过操作
        :param act_params:
        :return:
        """
        logger.debug(u"过操作: %s", str(act_params))

        for step in self.game_config.player_act_step.get(Act.GUO):
            for name, cfg in step.items():
                ret = self.step_handlers.get(name)(seat_id=self.seat_id, act_params=act_params, config_params=cfg)
                if not ret:
                    logger.error("step:%s", step)
                    return
        return 1

    def param_check(self, **kwargs):      # 参数验证
        act_params = kwargs.get("act_params")
        if 1 > len(act_params) or not self.game_data.next_speaker_callback:
            logger.debug(u"act_guo_error:%s", str([act_params, self.game_data.next_speaker_callback]))
            return
        self.seat_id = list(act_params.keys())[0]
        return 1

    def set_data(self, **kwargs):      # 设置关键参数
        # 针对过户操作, 如果玩家在听牌情况下选择过,则过户次数+1
        is_ting = self.players[self.seat_id].hand_card.is_ting
        ting_cards = self.players[self.seat_id].ting_info.keys()
        cur_op_card = self.game_data.cur_deal_card_val
        if is_ting and cur_op_card in ting_cards and self.game_config.pass_hu_double:
            guo_hu_card = self.game_data.last_get_card_val[self.seat_id]
            self.players[self.seat_id].hand_card.guo_hu_num += 1
            act_info = {"seat_id": self.seat_id,
                        "act_type": Act.GUO_HU_DOUBLE,
                        "card_list": [guo_hu_card]}
            self.notify_other_player_act_executed(self.seat_id,
                                                  act_info=act_info,
                                                  max_player_num=self.game_data.max_player_num)
        return 1

    def next_act(self, **kwargs):  # 通知桌子进行下一步操作
        c_type = self.game_data.next_speaker_callback.get('type')
        call_params = self.game_data.next_speaker_callback.get("call_params")
        print("guo, next_act:", self.game_data.next_speaker_callback)
        self.game_data.next_speaker_callback = {}
        CallbackManager.get_instance(self.desk_id).execute(call_func_type=c_type, call_params=call_params)

        # if GameActStatus.AFTER_DRAW_CARD == self.game_data.last_game_act_status["status"]:
        #     # 摸牌後当前用户进行下一步操作（出牌）
        #     self.notify_player_to_act(self.game_data.last_game_act_status["seat_id"], act_info={Act.CHU: {}},
        #                               interval=self.get_act_wait_time(self.game_data.last_game_act_status["seat_id"]))
        # else:
        #     # 出牌後桌子進行下一步操作　
        #     return self.system_act(SystemActType.DRAW_CARD
        #                        , act_params={"seat_id": self.game_data.last_game_act_status["seat_id"]})
