# coding=utf-8

import math

from service.room.handlers.basehandler import BaseHandler, RegisterEvent
from share.message_ids import *
from service.room.validators.friend_desk.dissolve_desk_answer import DissolveDeskAnswerValidator
from service.room.common_define import DeskStatus
from service.room.models.room_manager import room_mgr


@RegisterEvent(DISSOLVE_DESK_ANSWER)
class DissolveDeskAnswerHandler(BaseHandler):

    def execute(self, *args, **kwargs):
        """
        玩家对其他玩家请求解散桌子的响应
        :param args:
        :param kwargs:
        :return: {need_agree: 0/1} 发生错误0, 1表示需要其他玩家同意
        """
        validator = DissolveDeskAnswerValidator(handler=self)

        answer_dissolve_desk(validator.desk, validator.user, validator.agree.data)

        return {'need_push': 0}


def answer_dissolve_desk(desk, user, agree=1, is_auto=0):
    """
    回应其他玩家解散房间的请求
    :param desk: 桌子object
    :param user: 玩家object
    :param agree:
    :param is_auto: 是否超时自动操作
    :return:
    """
    if is_auto:
        # 托管后操作如果玩家已操作完，则忽略
        if not desk or not user or user.user_id in desk.dissolve_agreed_users \
                or user.user_id in desk.dissolve_reject_users:
            return

    if 1 == agree:
        desk.dissolve_agreed_users.append(user.user_id)
        if len(desk.dissolve_agreed_users) > desk.max_player_num / 2:
            # 多数玩家同意解散, 执行解散桌子
            data = {"user_id": user.user_id, "nick": user.nick_name, "agree": agree, "success": 1}
            desk.notify_player(user.seat_id, DISSOLVE_DESK_ANSWER, data)  # 首先响应当次请求处理成功
            desk.notify_desk(PUSH_DESK_DISSOLVE_RESULT, data)
            room_mgr.del_desk(desk.desk_id)
        else:
            # 通知其他玩家该玩家的响应
            data = {"user_id": user.user_id, "nick": user.nick_name, "agree": agree}
            desk.notify_desk_some_user(PUSH_DESK_DISSOLVE_ANSWER, data, [user.user_id])
            desk.notify_player(user.seat_id, DISSOLVE_DESK_ANSWER, data)
    else:
        desk.dissolve_reject_users.append(user.user_id)
        if len(desk.dissolve_reject_users) >= int(math.ceil(desk.max_player_num / 2.0)):
            # 半数或半数以上玩家拒绝解散
            data = {"user_id": user.user_id, "nick": user.nick_name, "agree": agree, "success": 0}
            desk.notify_player(user.seat_id, DISSOLVE_DESK_ANSWER, data)  # 首先响应当次请求处理成功
            desk.notify_desk(PUSH_DESK_DISSOLVE_RESULT, data)
            desk.dissolve_agreed_users = []
            desk.dissolve_reject_users = []
        else:
            # 通知其他玩家该玩家的响应
            data = {"user_id": user.user_id, "nick": user.nick_name, "agree": agree}
            desk.notify_desk_some_user(PUSH_DESK_DISSOLVE_ANSWER, data, [user.user_id])
            desk.notify_player(user.seat_id, DISSOLVE_DESK_ANSWER, data)

