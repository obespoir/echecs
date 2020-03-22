# coding=utf-8

from wtforms import fields, validators

from service.room.validators.basevalidator import BaseValidator
from service.room.models.room_manager import room_mgr
from service.room.common_define import UserStatus
from share import errorcode


class UserOfflineValidator(BaseValidator):

    session_id = fields.StringField("session_id")

    @property
    def user(self):
        return self.handler.cur_user_from_manager

    @property
    def desk(self):
        return room_mgr.get_desk_by_user_id(self.user.user_id)

    def validate_session_id(self, field):
        if not self.user or self.user.status == UserStatus.OFFLINE:
            raise validators.ValidationError(errorcode.USER_NOT_FOUND_ON_DESK)

        if not self.desk:
            raise validators.ValidationError(errorcode.DESK_NOT_EXIST)