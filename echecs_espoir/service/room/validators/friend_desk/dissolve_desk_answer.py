# coding=utf-8

from wtforms import fields, validators

from service.room.validators.basevalidator import BaseValidator
from service.room.models.room_manager import room_mgr
from share import errorcode


class DissolveDeskAnswerValidator(BaseValidator):
    agree = fields.IntegerField("agree", default=1)

    @property
    def user(self):
        return self.handler.cur_user_from_manager

    @property
    def desk(self):
        return room_mgr.get_desk_by_user_id(self.user.user_id)

    def validate_agree(self, field):
        if not self.user:
            raise validators.ValidationError(errorcode.USER_NOT_FOUND_ON_DESK)

        if not self.desk:
            raise validators.ValidationError(errorcode.DESK_NOT_EXIST)

        if not self.desk.dissolve_agreed_users:
            # 没有玩家申请过解散房间
            raise validators.ValidationError(errorcode.INVALID_REQUEST)

        if self.user.user_id in self.desk.dissolve_agreed_users or self.user.user_id in self.desk.dissolve_reject_users:
            # 玩家已经作出过响应, 重复请求
            raise validators.ValidationError(errorcode.REPEAT_REQUEST)

