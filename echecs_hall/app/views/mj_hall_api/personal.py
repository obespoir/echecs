# coding=utf-8
from app.views.base_handler import BaseHandler
import json
from . import mj_hall
from app.controller.mj_hall_controller import login_hall_controller
from app.share.error_code import *
import time
from app.extensions.common import md5
from tornado.web import authenticated


@mj_hall.route('/getpersonal')
class GetPersonal(BaseHandler):
    isLogin = True
    tag = __name__

    @authenticated
    def get(self):
        # 获取玩家信息
        user = self.current_user
        uid = int(user['uid'])
        user_money = int(user['money'])
        user_diamond = int(user['diamond'])
        nick_name = user['nick_name']
        avater_url = user['avater_url']

        # 获取牌局信息
        game_info = login_hall_controller.get_match_data_in_cache(uid)
        print(game_info)
        # 总局数
        total = int(game_info['win_count']) + int(game_info['lose_count'])

        # 胜率
        if int(total) == 0:
            winning_rate = str(total) + '%'
        else:
            winning_rate = str(round(float(game_info['win_count']) / float(total), 2) * 100) + '%'


        # 最高连胜
        highest_winning_streak = int(game_info['highest_winning_streak'])

        data = {'uid': uid, 'money': user_money, 'diamond': user_diamond, 'nick_name': nick_name,
                'avater_url': avater_url, 'total': total, 'winning_rate': winning_rate,
                'highest_winning_streak': highest_winning_streak}
        print("data=", data)
        self.return_success(data)

    def post(self):
        pass

@mj_hall.route('/getcurrency')
class GetCurrency(BaseHandler):
    isLogin = True
    tag = __name__

    @authenticated
    def get(self):
        user = self.current_user
        uid = int(user['uid'])
        user_money = int(user['money'])
        user_diamond = int(user['diamond'])
        data = {'money': user_money, 'diamond': user_diamond}
        self.return_success(data)

    def post(self):
        pass

