# coding=utf-8

from wtforms import fields, validators

from service.room.validators.basevalidator import BaseValidator
from service.room.models.room_manager import room_mgr
from service.room.common_define import UserStatus, DeskStatus
from service.room.models.user_manager import UserManager
from share import errorcode


class UserExitValidator(BaseValidator):
    x = fields.StringField()
    session_id = fields.StringField("session_id")

    @property
    def user(self):
        return self.handler.cur_user_from_manager

    @property
    def desk(self):
        return room_mgr.get_desk_by_user_id(self.user.user_id)

    def validate_session_id(self, field):
        if not UserManager().get_user_by_sessionid(self.session_id.data):
            raise validators.ValidationError(errorcode.USER_NOT_FOUND_ON_DESK)

    def validate_x(self, field):
        if not self.user:
            raise validators.ValidationError(errorcode.USER_NOT_FOUND_ON_DESK)

        if not self.desk:
            raise validators.ValidationError(errorcode.DESK_NOT_EXIST)

        if self.desk.status == DeskStatus.PLAYING:
            raise validators.ValidationError(errorcode.DESK_IS_PLAYING)
