# coding=utf-8

from wtforms import fields, validators

from service.room.validators.basevalidator import BaseValidator
from service.room.models.room_manager import room_mgr
from service.room.common_define import UserStatus
from service.room.models.user_manager import UserManager
from share import errorcode



class UserReadyValidator(BaseValidator):
    ready = fields.IntegerField("ready", default=1)
    session_id = fields.StringField("session_id")

    @property
    def user(self):
        return self.handler.cur_user_from_manager

    @property
    def desk(self):
        return room_mgr.get_desk_by_user_id(self.user.user_id)

    def validate_ready(self, field):
        print("vvvvvvvvvvv:")
        if not self.user:
            raise validators.ValidationError(errorcode.USER_NOT_FOUND_ON_DESK)
        print("vvvvvvvvvvv22222:")
        if not self.desk:
            raise validators.ValidationError(errorcode.DESK_NOT_EXIST)
        print("vvvvvvvvvvv333333:")
        if self.ready.data == 1 and self.user.status == UserStatus.READY or \
                                self.ready.data != 1 and self.user.status == UserStatus.UNREADY:
            # 玩家已经作出过响应, 重复请求
            raise validators.ValidationError(errorcode.REPEAT_REQUEST)

    def validate_session_id(self, field):
        print("vvvvvvvvvvv444444:")
        if not UserManager().get_user_by_sessionid(self.session_id.data):
            raise validators.ValidationError(errorcode.USER_NOT_FOUND_ON_DESK)

        print("vvvvvvvvvvv555555:")