# coding=utf-8

from service.room.common_define import DeskStatus, DeskType
from service.room.handlers.basehandler import BaseHandler, RegisterEvent
from service.room.models.user_manager import UserManager
from service.room.validators.user_offline import UserOfflineValidator
# from service.session_gate_rel import session_gate_ins
from share.message_ids import *
from share.notify_web_server import notify_web_server_left_room


@RegisterEvent(USER_OFFLINE)
class UserOfflineHandler(BaseHandler):

    def execute(self, *args, **kwargs):
        """
        玩家断线
        :param args:
        :param kwargs:
        :return:
        """
        validator = UserOfflineValidator(handler=self)
        validator.user.set_offline()
        # session_gate_ins.del_rel(validator.session_id.data)
        data = {"user_id": validator.user.user_id, "nick": validator.user.nick_name, "is_offline": validator.user.is_offline}
        validator.desk.notify_desk_some_user(PUSH_USER_STATUS, data, [validator.user.user_id])
        if validator.desk.status != DeskStatus.PLAYING and validator.desk.desk_type == DeskType.MATCH_DESK:
            print("game.status != playing!")
            validator.desk.user_exit(validator.user.user_id)
            UserManager().exit_user(validator.user.user_id)

        return {"need_push": 0}
