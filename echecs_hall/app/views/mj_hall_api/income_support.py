# coding=utf-8
from app.views.base_handler import BaseHandler
import json
from . import mj_hall
from app.share.error_code import *
import time
from app.extensions.common import md5, diff_days, diff_hours
from tornado.web import authenticated
from app.controller.mj_hall_controller import income_support_controller
from app.controller.mj_hall_controller import login_hall_controller


@mj_hall.route('/receiveincomesupport')
class ReceiveIncomeSupport(BaseHandler):
    isLogin = True
    tag = __name__

    @authenticated
    def get(self):
        user = self.current_user
        uid = user['uid']
        user_money = int(user['money'])
        now = int(time.time())

        # 判断是否符合条件领取破产补助
        # 补助金额
        money = int(self.application.game_config['income_support'])
        # 领取补助金额间隔时间
        get_income_support_interval = int(self.application.game_config['get_income_support_interval'])

        if income_support_controller.get_income_support_by_uid(uid):
            # 玩家领取破产补助详情
            income_support_info = income_support_controller.get_income_support_by_uid(uid)

            id = income_support_info['id']
            collection_time = int(income_support_info['collection_time'])
            income_support_times = int(income_support_info['income_support_times'])

            if now - collection_time > get_income_support_interval:
                if income_support_times < 3:
                    data = {'uid': uid, 'collection_time': now,
                            'income_support_times': int(income_support_info['income_support_times']) + 1}
                    if income_support_controller.update_income_support_by_id(id, data):
                        if login_hall_controller.update_user_in_cache(uid, {'money': user_money + money}):
                            self.return_success({'money': user_money + money})
                else:
                    self.return_error(GET_INCOME_SUPPORT_THREE_TIME)
            else:
                self.return_error(GET_INCOME_SUPPORT_ERROR)

        else:
            data = {'uid': uid, 'collection_time': now, 'income_support_times': 1}
            if income_support_controller.save_income_support(data) > 0:
                if login_hall_controller.update_user_in_cache(uid, {'money': user_money+money}):
                    self.return_success({'money': user_money+money})
            else:
                self.return_error(INSERT_ERROR)

    def post(self):
        pass


@mj_hall.route('/getincomesupport')
class GetIncomeSupport(BaseHandler):
    isLogin = True
    tag = __name__

    @authenticated
    def get(self):
        user = self.current_user
        uid = user['uid']
        now = time.time()

        # 补助金额
        money = int(self.application.game_config['income_support'])

        # 领取补助金额间隔时间
        get_income_support_interval = int(self.application.game_config['get_income_support_interval'])

        if income_support_controller.get_income_support_by_uid(uid):
            # 玩家领取破产补助详情
            income_support_info = income_support_controller.get_income_support_by_uid(uid)

            collection_time = int(income_support_info['collection_time'])
            income_support_times = int(income_support_info['income_support_times'])

            if now - collection_time > get_income_support_interval:
                if income_support_times < 3:
                    data = {'money': money,
                            'income_support_times': int(income_support_info['income_support_times']) + 1}
                    self.return_success(data)
                else:
                    self.return_error(GET_INCOME_SUPPORT_THREE_TIME)
            else:
                self.return_error(GET_INCOME_SUPPORT_ERROR)
        else:
            data = {'money': money, 'income_support_times': 1}
            self.return_success(data)

    def post(self):
        pass

