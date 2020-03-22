# coding=utf-8

from wtforms import fields, validators

from service.room.validators.basevalidator import BaseValidator
from service.room.models.room_manager import room_mgr
from service.room.common_define import UserStatus, DeskStatus
from share import errorcode


class UserReconnectValidator(BaseValidator):
    x = fields.StringField()
    user_id = fields.IntegerField("user_id")
    session_id = fields.StringField("session_id")

    @property
    def user(self):
        return self.handler.cur_user_from_manager_by_id(self.user_id.data)

    @property
    def desk(self):
        return room_mgr.get_desk_by_user_id(self.user.user_id)

    def validate_x(self, f):
        if not self.user:
            raise validators.ValidationError(errorcode.USER_NOT_FOUND_ON_DESK)

        if not self.desk:
            raise validators.ValidationError(errorcode.DESK_NOT_EXIST)