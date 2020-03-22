# coding=utf-8

from service.room.handlers.basehandler import BaseHandler, RegisterEvent
from service.room.validators.user_exit import UserExitValidator
from service.room.models.user_manager import UserManager
# from service.session_gate_rel import session_gate_ins
from share.message_ids import *


@RegisterEvent(USER_EXIT_DESK)
class UserExitHandler(BaseHandler):

    def execute(self, *args, **kwargs):
        """
        玩家请求退出桌子
        :param args:
        :param kwargs:
        :return:
        """
        validator = UserExitValidator(handler=self)
        data = validator.user.to_dict()
        validator.desk.notify_desk_some_user(PUSH_USER_EXIT, data, [validator.user.user_id])
        # session_gate_ins.del_rel(validator.session_id.data)
        validator.desk.user_exit(validator.user.user_id)
        UserManager().exit_user(validator.user.user_id)

        return {"code": 200}
