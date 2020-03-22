# coding=utf-8
from app.views.base_handler import BaseHandler
from app.controller.mj_hall_controller import login_hall_controller
from app.controller.mj_hall_controller import email_controller
import json
from . import mj_hall
from app.share.error_code import *
import time, random
from app.extensions.common import md5


@mj_hall.route('/register')
class RegisterHandler(BaseHandler):
    isLogin = False
    tag = __name__



    def get(self):
        param = json.loads(self.get_argument('base'))
        user_name = self.get_param('user', param)
        password = self.get_param('password', param)
        nickname = self.get_param('nickname', param)

        if login_hall_controller.check_user_is_exist(user_name):
            self.return_error(REGISTER_ERROR)

        now = int(time.time())
        salt = '123456'
        skey = md5(str(now) + salt)
        password = md5(password + salt)
        ip = self.ip
        index = str(random.randint(1, 7)) + '.png'

        user = {'bsfb_id': '1', 'nick_name': nickname, 'user_name': user_name, 'password': password, 'sex': 1,
                'avater_url': 'http://ozgj3gqsu.bkt.clouddn.com/user1.png' + index, 'salt': salt, 'status': 1, 'skey': skey,
                'register_time': now, 'login_time': now, 'logout_time': now,
                'register_ip': ip, 'login_ip': ip, 'is_visitor': 1, 'is_vip': 0,
                'is_robot': 0, 'login_days': 0, 'is_get_login_reward': 0, 'platform_type': 1,
                'imei': 'ABC-123', 'device_num': 'ABC-456', 'agent': 'baidu', 'payment': 1, 'point': 0,
                'diamond': 1000, 'money': 10000, 'can_change_nickname': 0, 'need_binding': 0, 'phone': '15113456754'}

        uid = int(login_hall_controller.save_user(user))
        if uid > 0:
            user['uid'] = uid
            if int(login_hall_controller.save_user_info(user)) > 0:
                    self.return_success(user)
        else:
            self.return_error(REGISTER_PARAM_ERROR)

    def post(self):
        pass


@mj_hall.route('/login')
class LoginHandler(BaseHandler):
    isLogin = False
    tag = __name__

    def get(self):
        return self.write("login!!")

    def post(self):
        flag = 1
        param = json.loads(self.request.body)
        username = self.get_param('user', param)
        password = self.get_param('password', param)

        # 判断玩家账户,密码,状态
        user_id = 0
        salt = ''
        user_info = login_hall_controller.get_user_info_by_username(username)
        if user_info:
            if login_hall_controller.validate_password(username, password):
                if int(user_info['status']) == 1:
                    user_id = user_info['uid']
                    salt = user_info['salt']
                else:
                    self.return_error(USER_STATUS_PARAM_ERROR)
            else:
                self.return_error(PASSWORD_PARAM_ERROR)
        else:
            self.return_error(USER_PARAM_ERROR)

        # 判断用户是否存在缓存
        if not login_hall_controller.get_user_info_in_cache(user_id):
            if not login_hall_controller.save_user_info_in_cache(user_id, user_info):
                self.return_error(USER_SAVE_CACHE_ERROR)

        # 判断游戏记录是否存在缓存
        if not login_hall_controller.get_match_data_in_cache(user_id):
            if login_hall_controller.get_match_data_by_uid(user_id):
                match_data = login_hall_controller.get_match_data_by_uid(user_id)
                match_data.pop('id')
            else:
                match_data = {'uid': user_id, 'win_count': 0, 'lose_count': 0,
                              'winning_streak': 0, 'highest_winning_streak': 0}
            login_hall_controller.save_match_data_in_cache(user_id, match_data)

        # 判断游戏规则是否存在缓存
        if not login_hall_controller.get_game_rule_in_cache(user_id):
            if login_hall_controller.get_game_rule_by_uid(user_id):
                game_rule = login_hall_controller.get_game_rule_by_uid(user_id)
                game_rule.pop('id')
            else:
                game_rule = {'uid': user_id, 'useQuanPinDao': 0, 'useJiaMa': 0, 'useJiaPiao': 0,
                             'area': 0, 'useMaxFan': 8, 'chaDaJiao': 0, 'buFenLiang': 0,
                             'shuKan': 0, 'shao12BuLiang': 0, 'play_times_limit': 9999
                             }
            login_hall_controller.save_game_rule_in_cache(user_id, game_rule)

        # 更新登录时间与skey
        now = int(time.time())
        skey = md5(str(now) + salt)
        ip = self.request.remote_ip
        new_data = {'update_time': now, 'heartbeat_at': now, 'skey': skey, 'login_ip': ip}
        login_hall_controller.update_user_in_cache(user_id, new_data)

        info = login_hall_controller.get_user_info_in_cache(user_id)

        # 获取游戏服务参数
        config = self.application.game_config

        user_info = {'uid': int(info['uid']), 'user_name': info['user_name'], 'nick_name': info['nick_name'],
                     'bsfb_id': int(info['bsfb_id']), 'sex': int(info['sex']), 'password': info['password'],
                     'avater_url': info['avater_url'], 'payment': int(info['payment']),
                     'ip': config['game_server_config']['host'],
                     'port': int(config['game_server_config']['port']),
                     'diamond': int(info['diamond']), 'point': int(info['point']), 'skey': skey,
                     'is_visitor': int(info['is_visitor']), 'money': int(info['money'])
                     }
        # print user_info
        self.return_success(user_info)