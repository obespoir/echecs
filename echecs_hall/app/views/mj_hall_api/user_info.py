# coding=utf-8
from tornado.web import authenticated

from app.views.base_handler import BaseHandler
import json
from . import mj_hall
from app.controller.mj_hall_controller.user_info_controler import get_user_info_by_id


@mj_hall.route('/get_userinfo')
class GetUserInfo(BaseHandler):
    isLogin = True
    tag = __name__

    @authenticated
    def get(self):
        print("GetUserInfo self=", self)
        param = json.loads(self.get_argument('base'))
        uid = param['param']["base"]["uid"]
        ret = get_user_info_by_id(uid)
        print("GetUserInfo ret=", ret)
        r = {
            "nick_name": ret.get("nick_name"),
            "uid": ret.get("uid"),
            "money": ret.get("money"),
            "diamond": ret.get("diamond"),
            "total": ret.get("play_count", 0),
            "winning_rate": ret.get("win_percent", 0),
            "highest_winning_streak": ret.get("max_wins", 0),
            "avater_url": ret.get("avater_url", 'http://ozgj3gqsu.bkt.clouddn.com/user3.png')
        }
        print("data=", r)
        self.return_success(r)

    def post(self):
        pass