# coding=utf-8
from ..base_handler import BaseHandler
from . import admin

@admin.route("/status",name="status")
class StatusHandler(BaseHandler):
    def get(self):
        return self.write("status!")