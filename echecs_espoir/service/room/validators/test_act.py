# coding=utf-8

from wtforms import fields, validators
import ujson

from service.room.validators.basevalidator import BaseValidator
from service.room.models.room_manager import room_mgr
from share import errorcode


class TestActValidator(BaseValidator):
    test_type = fields.IntegerField("test_type")
    test_params = fields.StringField("test_params")

    @property
    def user(self):
        return self.handler.cur_user_from_manager

    @property
    def desk(self):
        return room_mgr.get_desk_by_user_id(self.user.user_id)

    def validate_test_params(self, field):
        if not self.user:
            raise validators.ValidationError(errorcode.USER_NOT_FOUND_ON_DESK)

        if not self.desk:
            raise validators.ValidationError(errorcode.DESK_NOT_EXIST)

        try:
            self.test_params.data = ujson.loads(field.data)
            if not isinstance(self.test_params.data.get("source_card"),list) or not isinstance(self.test_params.data.get("target_card"), list):
                raise validators.ValidationError(errorcode.PARAMS_ERROR)
        except Exception:
            raise validators.ValidationError(errorcode.PARAMS_ERROR)