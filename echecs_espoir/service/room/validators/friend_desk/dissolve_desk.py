# coding=utf-8

from wtforms import fields, validators

from service.room.validators.basevalidator import BaseValidator
from service.room.models.room_manager import room_mgr
from service.room.models.user_manager import UserManager
from share import errorcode


class DissolveDeskValidator(BaseValidator):
    x = fields.StringField()
    user_id = fields.StringField("user_id")
    session_id = fields.StringField("session_id")

    @property
    def user(self):
        _user= UserManager().get_user_by_id(int(self.user_id.data))
        return _user

    @property
    def desk(self):
        return room_mgr.get_desk_by_user_id(int(self.user_id.data))

    @property
    def desk_user_ids(self):
        ret = []
        for i in self.desk.users:
            if i:
                ret.append(i.user_id)
        return ret


    def validate_x(self, field):
        if not self.user:
            raise validators.ValidationError(errorcode.USER_NOT_FOUND_ON_DESK)

        if not self.desk:
            raise validators.ValidationError(errorcode.DESK_NOT_EXIST)

    def validate_session_id(self, field):
        if not self.session_id.data:
            raise validators.ValidationError(errorcode.SESSION_NOT_EXIST)

    def validate_user_id(self, field):
        if UserManager().get_user_by_id(self.user_id.data):
            raise validators.ValidationError(errorcode.USER_IN_OTHER_DESK)
