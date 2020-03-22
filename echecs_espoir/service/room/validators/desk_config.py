# coding=utf-8

from wtforms import fields, validators
import ujson

from service.room.validators.basevalidator import BaseValidator
from service.room.models.room_manager import room_mgr
from service.room.common_define import UserStatus, DeskStatus
from share import errorcode


class DeskConfigValidator(BaseValidator):
    custom_config = fields.StringField("custom_config")

    @property
    def user(self):
        return self.handler.cur_user_from_manager

    @property
    def desk(self):
        return room_mgr.get_desk_by_user_id(self.user.user_id)

    def validate_custom_config(self):
        if not self.user:
            raise validators.ValidationError(errorcode.USER_NOT_FOUND_ON_DESK)

        if not self.desk:
            raise validators.ValidationError(errorcode.DESK_NOT_EXIST)

        if not self.desk.status != DeskStatus.READY:
            raise validators.ValidationError(errorcode.INVALID_REQUEST)

        try:
            config = ujson.loads(self.custom_config.data)
            self.custom_config.data = config
        except Exception:
            raise validators.ValidationError(errorcode.DESK_CONFIG_ERROR)
