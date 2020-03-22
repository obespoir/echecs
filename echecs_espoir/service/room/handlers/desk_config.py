# coding=utf-8

from service.room.handlers.basehandler import BaseHandler, RegisterEvent
from service.room.validators.desk_config import DeskConfigValidator
from service.room.common_define import DeskStatus, UserStatus
from service.room.models.room_manager import room_mgr
from share.message_ids import *


@RegisterEvent(USER_SET_CONFIG)
class DeskConfigHandler(BaseHandler):

    def execute(self, *args, **kwargs):
        """
        设置桌子配置
        :param args:
        :param kwargs:
        :return:
        """
        validator = DeskConfigValidator(handler=self)

        validator.desk.set_custom_config(validator.custom_config.data)

        data = {"user_id": validator.user.user_id, "nick": validator.user.nick_name,
                "config": validator.custom_config.data}
        validator.desk.notify_desk_some_user(PUSH_USER_SET_CONFIG, data, [validator.user.user_id])

        return {"config": validator.custom_config.data}
