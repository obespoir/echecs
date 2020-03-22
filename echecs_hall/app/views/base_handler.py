# coding=utf-8
from app.share.error_code import *
from tornado import web
from app.models.test_user import TestUser
from app.controller.mj_hall_controller import login_hall_controller
from tornado.web import HTTPError
import json


class BaseHandler(web.RequestHandler):

    data = {
        "ret": 0,
        "command_id": 0,
        "data": None
    }

    tag = __name__
    ip = ''

    def initialize(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.ip = self.request.remote_ip

    def get_ret(self, code, info=None):
        """
        获取返回结果
        :param code:
        :param command_id:
        :return:
        """
        if code < 1000:
            self.data["ret"] = code
            self.data["data"] = {}
            self.data["desc"] = ERROR_CODE_DESC[code]
        if info and isinstance(info, dict):
            for k, v in info.items():
                self.data.get("data")[k] = v
        return self.data

    def return_error(self, ret):
        desc = HALL_ERROR_CODE_DESC[ret]
        res = {'ret': int(ret), 'desc': desc, 'action': self.tag}
        print(res)
        self.finish(res)
        raise HTTPError(ret)

    def return_success(self, data):
        res = {'ret': 0, 'desc': 'success', 'data': data, 'action': self.tag}
        self.finish(res)

    def return_data(self, ret, data):
        desc = HALL_ERROR_CODE_DESC[ret]
        res = {'ret': int(ret), 'desc': desc, 'data': data, 'action': self.tag}
        return res

    def get_param(self, key, params):
        if key in params:
            return params[key]
        else:
            self.return_error(PARAM_ERROR)

    def get_current_user(self):
        param = json.loads(self.get_argument('base'))
        uid = self.get_param('uid', param)
        skey = self.get_param('skey', param)
        user = login_hall_controller.get_user_info_in_cache(uid)
        if user:
            if user['skey'] != skey:
                self.return_error(HALL_LOGIN_ERROR)
            return user
        else:
            self.return_error(NOT_LOGIN)
