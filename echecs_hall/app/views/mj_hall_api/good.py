# coding=utf-8
from app.views.base_handler import BaseHandler
from app.controller.mj_hall_controller import good_controller
from app.controller.mj_hall_controller import login_hall_controller
import json
from . import mj_hall
from app.share.error_code import *
import time
from app.extensions.common import md5
from tornado.web import authenticated


@mj_hall.route('/setgood')
class SetGood(BaseHandler):

    def get(self):
        print('good')

    def post(self):
        pass


@mj_hall.route('/getgood')
class GetGood(BaseHandler):
    isLogin = True
    tag = __name__

    @authenticated
    def get(self):
        data = []
        goods_list = good_controller.get_all_good_info()

        if not good_controller.get_all_good_info():
            self.return_data(NOT_GOODS, data)

        for good in goods_list:
            data.append({'id': good['id'], 'title': good['name'], 'rmb_price': good['rmb_price'],
                         'icon': good['icon'],
                         'selling_price': good['selling_price']})
        self.return_success(data)

    def post(self):
        pass


@mj_hall.route('/buygood')
class BuyGood(BaseHandler):
    isLogin = True
    tag = __name__

    @authenticated
    def get(self):
        param = json.loads(self.get_argument('base'))
        sub_param = param['param']
        good_id = int(self.get_param('id', sub_param))

        # 获取玩家信息
        user = self.current_user
        uid = int(user['uid'])
        user_money = int(user['money'])
        user_diamond = int(user['diamond'])

        # 根据id获取商品信息
        good_info = good_controller.get_good_info_by_id(good_id)

        # 商品价格
        selling_price = int(good_info['selling_price'])

        # 商品数量
        quantity = int(good_info['quantity'])

        if not good_info:
            self.return_error(PARAM_ERROR)

        # 判断玩家钻石是否够买此商品
        if user_diamond >= selling_price:
            diamond = user_diamond - selling_price
            money = user_money + quantity
            data = {'diamond': diamond, 'money': money}
            login_hall_controller.update_user_in_cache(uid, data)
            self.return_success(data)
        else:
            self.return_error(NOT_ENOUGH_DIAMOND)

    def post(self):
        pass
