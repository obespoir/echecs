# coding=utf-8

from ...extensions.blueprint import Blueprint
admin = Blueprint("admin", url_prefix="/admin")
import app.views.admin.login_handler
import app.views.admin.status_handler
