# coding=utf-8

from service.room.models.user_manager import UserManager
from service.room.validators.basevalidator import BaseValidator
from share.notify_web_server import notify_web_server_join_room
from share import errorcode
from wtforms import fields, validators


class JoinMatchDeskByTypeValidator(BaseValidator):
    x = fields.StringField()
    user_id = fields.IntegerField("user_id")
    room_type = fields.IntegerField("room_type")
    session_id = fields.StringField("session_id")

    def validate_user_id(self, field):
        if UserManager().get_user_by_id(self.user_id.data):
            raise validators.ValidationError(errorcode.USER_IN_OTHER_DESK)

    def validate_session_id(self, field):
        if not self.session_id.data:
            raise validators.ValidationError(errorcode.USER_IN_OTHER_DESK)

    def validate_room_type(self, field):
        if int(self.room_type.data) not in [0, 1, 2]:
            raise validators.ValidationError(errorcode.ROOM_TYPE_ERROR)

    def validate_x(self, field):
        r = notify_web_server_join_room(self.user_id.data, self.session_id.data, self.room_type.data)
        print("JoinMatchDeskByTypeHandler r =", r)
        code = r["data"].get("code")
        if code:
            raise validators.ValidationError(code)