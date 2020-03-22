# coding=utf8

from wtforms import fields, validators

from db.mysql.user import User
from service.room.validators.basevalidator import BaseValidator


class LoginValidator(BaseValidator):
    user_id = fields.IntegerField("user_id", [validators.DataRequired()])
    password_hash = fields.StringField("password_hash", [validators.DataRequired()])

    @property
    def user(self):
        return User.objects.filter(uid=self.user_id.data).first()

    def validate_user_id(self, field):
        if not self.user:
            raise validators.ValidationError("")

    def validate_password_hash(self, field):
        if field.data != self.user.passwd:
            raise validators.ValidationError("")
