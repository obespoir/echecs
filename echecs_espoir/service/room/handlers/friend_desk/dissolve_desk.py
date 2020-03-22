# coding=utf-8

from service.room.handlers.basehandler import BaseHandler, RegisterEvent
from service.room.validators.friend_desk.dissolve_desk import DissolveDeskValidator
from service.room.common_define import DeskStatus
from service.room.models.room_manager import room_mgr
from share.message_ids import *
from share.timer_task import TimerTask
from config.globalconfig import GlobalConfig
from service.room.handlers.friend_desk.dissolve_desk_answer import answer_dissolve_desk


@RegisterEvent(DISSOLVE_FRIEND_DESK)
class DissolveDeskHandler(BaseHandler):

    def execute(self, *args, **kwargs):
        """
        解散桌子请求处理
        :param args:
        :param kwargs:
        :return: {need_agree: 0/1} 成功退出时0, 1表示需要其他玩家同意
        """
        validator = DissolveDeskValidator(handler=self)

        if validator.desk.is_last_round() and DeskStatus.PLAYING != validator.desk.status:
            # 最后一局结束，此时直接退出桌子
            if validator.user.seat_id == validator.desk.owner_seat:
                # 房主退出, 桌子直接解散
                response_data = {"need_agree": 0}
                validator.desk.notify_player(validator.user.seat_id, DISSOLVE_FRIEND_DESK, response_data)

                data = {"user_id": validator.user.user_id, "nick": validator.user.nick_name, "success": 1}
                validator.desk.notify_desk(PUSH_DESK_DISSOLVE_RESULT, data)
                room_mgr.del_desk(validator.desk.desk_id)
            else:
                data = {"user_id": validator.user.user_id, "nick": validator.user.nick_name}
                validator.desk.notify_desk_some_user(PUSH_USER_EXIT, data, [validator.user.user_id])
                room_mgr.user_exit(validator.user.user_id)

                response_data = {"need_agree": 0}
                validator.desk.notify_player(validator.user.seat_id, DISSOLVE_FRIEND_DESK, response_data)
        else:
            # 不是最后一局,需要发送解散请求征询其他玩家同意
            data = {"user_id": validator.user.user_id, "nick": validator.user.nick_name}
            validator.desk.notify_desk_some_user(PUSH_DESK_DISSOLVE, data, [validator.user.user_id])
            TimerTask.call_later(GlobalConfig().dissolve_time,
                                 answer_dissolve_desk, validator.desk, validator.user, agree=1, is_auto=1)

            response_data = {"need_agree": 1}
            validator.desk.notify_player(validator.user.seat_id, DISSOLVE_FRIEND_DESK, response_data)

        return {"need_push": 0}
