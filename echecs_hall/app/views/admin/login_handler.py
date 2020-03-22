# coding=utf-
from . import admin
from ..base_handler import BaseHandler


@admin.route("/indexaaaaaaaaaaaaaaaaaaaaaaa", name="name")
class HomeHandler(BaseHandler):
    def get(self):
        return self.write("index!")
