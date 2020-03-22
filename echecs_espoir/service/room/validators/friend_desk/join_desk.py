# coding=utf-8

from wtforms import fields, validators

from service.room.validators.basevalidator import BaseValidator
from service.room.models.user_manager import UserManager
from service.room.models.roomdesk_manager import desk_mgr
from share import errorcode


class JoinDeskValidator(BaseValidator):
    user_id = fields.IntegerField("user_id")
    session_id = fields.StringField("session_id")
    desk_id = fields.IntegerField("desk_id")

    def validate_session_id(self, field):
        if UserManager().get_user_by_sessionid(self.session_id.data):
            raise validators.ValidationError(errorcode.USER_IN_OTHER_DESK)

    def validate_desk_id(self, field):
        desk = desk_mgr.get_room_desk(self.desk_id.data)
        if not desk:
            raise validators.ValidationError(errorcode.DESK_NOT_EXIST)

        if not desk.is_in_desk(self.user_id.data) and desk.is_full():
            raise validators.ValidationError(errorcode.DESK_IS_FULL)