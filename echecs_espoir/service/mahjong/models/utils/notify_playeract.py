# coding=utf-8

from service.mahjong.controls.notifybridge import notify_single_user
from service.mahjong.models.callbackmanager import CallbackFuncType
from service.mahjong.models.timermanager import timer_manager_ins
from obespoir.share.ob_log import logger
from service.mahjong.constants.gamedefine import TimerType
from share.message_ids import PUSH_CALL_CARD, PUSH_OTHER_PLAYER_CALL_CARD


class NotifyPlayerAct(object):
    """
    通知玩家进行可以操作
    """

    def __init__(self):
        pass

    def notify_player(self, desk_id, seat_id, act_info={}, interval=1000,t_type=TimerType.NORMAL, command_id=PUSH_CALL_CARD, code=200):
        """
        :param desk_id:
        :param seat_id:
        :param act_info: 玩家可进行的操作信息{act_type:params, ...}
        :param interval:
        :return:
        """
        logger.debug(u"通知玩家进行操作: %s", str([seat_id, act_info, interval]))
        data = {"seat_id": seat_id, "act_info": act_info}
        notify_single_user(desk_id, seat_id, command_id, data, code)
        timer_manager_ins.add_timer(desk_id, seat_id, interval,
                                    t_type=t_type,
                                    call_type=CallbackFuncType.FUNC_AUTO_PLAYER_ACT,
                                    call_params={"seat_id": seat_id, "act_info": act_info})

    def notify_some_player(self, desk_id, seat_id, act_info={}, interval=1000, max_player_num=4, exclude=[]):
        """
        推送给桌子上的某些用户, 用于玩家执行动作后的推送
        :param desk_id: 桌子ID
        :param seat_id: 执行动作的玩家位置
        :param act_info: 详细动作参数 {act_type:[card_val]}
        :param interval: 延迟时间
        :param exclude: 可以排除推送的作为ID, [seat_id,1]
        :return:
        """
        logger.debug(u"通知桌子上某些玩家: %s", str([exclude, act_info, interval]))
        target_seat_id = act_info.get("seat_id")
        act = list(act_info.keys())[0]
        for i in range(max_player_num):
            if not i in exclude:
                if i != target_seat_id and act == 60:
                    act_info["card_list"] = []
                notify_single_user(desk_id, i, PUSH_OTHER_PLAYER_CALL_CARD, act_info)
        # timer_manager_ins.add_timer(desk_id, seat_id, interval, call_type=CallbackFuncType.FUNC_AUTO_PLAYER_ACT
        #                             , call_params=act_info)

    def notify_some_player_ting(self, desk_id, seat_id, act_info={}, interval=1000, max_player_num=4):
        """
        推送给桌子上的某些用户, 用于玩家执行听牌后的推送
        :param desk_id: 桌子ID
        :param seat_id: 执行动作的玩家位置
        :param act_info: 详细动作参数 {act_type:[card_val]}
        :param interval: 延迟时间
        :return:
        """
        logger.debug(u"通知桌子上某些玩家: %s", str([desk_id,seat_id,act_info, interval]))
        act = list(act_info.keys())[0]
        for i in range(max_player_num):
            notify_single_user(desk_id, i, PUSH_OTHER_PLAYER_CALL_CARD, act_info)
        # timer_manager_ins.add_timer(desk_id, seat_id, interval, call_type=CallbackFuncType.FUNC_AUTO_PLAYER_ACT
        #                             , call_params=act_info)


notify_player_ins = NotifyPlayerAct()
