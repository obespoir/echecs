# coding=utf-8
from app.views.base_handler import BaseHandler
from app.controller.mj_hall_controller import email_controller
from app.controller.mj_hall_controller import reward_controller
from app.controller.mj_hall_controller import prop_controller
from app.controller.mj_hall_controller import login_hall_controller
import json
from . import mj_hall
from app.share.error_code import *
import time
from app.extensions.common import md5, diff_days, diff_hours
from tornado.web import authenticated
import operator


@mj_hall.route('/sendemail')
class SendEmail(BaseHandler):

    def get(self):
        param = json.loads(self.get_argument('base'))
        sub_param = param['param']

    def post(self):
        pass


@mj_hall.route('/getemail')
class GetEmail(BaseHandler):
    isLogin = True
    tag = __name__

    @authenticated
    def get(self):
        user = self.current_user
        uid = user['uid']
        data = []

        if not email_controller.validate_user_mail(uid):
            self.write(self.return_data(NOT_USER_EMAIL, data))
            return

        user_email = email_controller.get_user_mail_by_uid(uid)

        # 过滤不符合条件的邮件
        user_email = filter(self.filter_email, user_email)

        if len(user_email) < 1:
            self.write(self.return_data(NOT_MATCH_EMAIL, data))
            return

        # 按时间排序
        user_email.sort(key=operator.itemgetter('send_date'), reverse=True)

        # 获取全部邮件信息
        email_info = email_controller.get_all_email_info()
        new_email_info = {}
        for item in email_info:
            new_email_info[item['id']] = item

        for items in user_email:
            hours = diff_hours(int(items['send_date']))
            if hours < 1:
                time_desc = u'刚刚'
            elif hours <= 24:
                time_desc = str(int(hours)) + u'小时前'
            elif hours > 24:
                time_desc = time.strftime('%Y年%m月%d日', time.localtime(int(items['send_date'])))

            data.append({'title': new_email_info[items['eid']]['title'],
                         'content': new_email_info[items['eid']]['content'],
                         'icon': '',
                         'time_desc': time_desc,
                         'id': items['id']})

        self.return_success(data)

    @classmethod
    def filter_email(cls, data):
        return int(data['is_read']) != 9 and diff_days(int(data['send_date'])) < 30

    def post(self):
        pass


@mj_hall.route('/reademail')
class ReadEmail(BaseHandler):
    isLogin = True
    tag = __name__

    @authenticated
    def get(self):
        param = json.loads(self.get_argument('base'))
        sub_param = param['param']
        user_email_id = int(self.get_param('id', sub_param))

        user_email = email_controller.get_one_user_mail_by_id(user_email_id)
        if not user_email:
            self.return_error(PARAM_ERROR)

        # 获取全部邮件信息
        email_info = email_controller.get_all_email_info()
        new_email_info = {}
        for item in email_info:
            new_email_info[item['id']] = item

        # 判断是否符合条件的邮件
        if int(user_email['is_read']) != 9 and diff_days(int(user_email['send_date'])) < 30:
            data = {'title': new_email_info[user_email['eid']]['title'],
                    'content': new_email_info[user_email['eid']]['content'],
                    'id': user_email['id']}
            # 判断此邮件是否有奖励
            if new_email_info[user_email['eid']]['reward_id']:
                reward_id = new_email_info[user_email['eid']]['reward_id']
                # 获取奖励详情
                reward_list = reward_controller.get_all_reward_info()
                new_reward_list = {}
                for reward in reward_list:
                    new_reward_list[reward['id']] = reward

                # 获取道具详情
                prop_list = prop_controller.get_all_prop_info()
                new_prop_list = {}
                for prop in prop_list:
                    new_prop_list[prop['id']] = prop

                # print new_reward_list, new_prop_list
                user_reward = []
                for rid in reward_id.split(','):
                    rid = int(rid)
                    reward_name = new_prop_list[new_reward_list[rid]['prop_id']]['name']
                    reward_icon = new_prop_list[new_reward_list[rid]['prop_id']]['icon']
                    reward_quantity = new_reward_list[rid]['reward_quantity']
                    user_reward.append({'reward_name': reward_name, 'reward_icon': reward_icon,
                                        'reward_quantity': reward_quantity})
                data['reward'] = user_reward

            else:
                data['reward'] = []

            self.return_success(data)

        else:
            self.return_error(PARAM_ERROR)

    def post(self):
        pass


@mj_hall.route('/confirmemail')
class ConfirmEmail(BaseHandler):
    isLogin = True
    tag = __name__

    @authenticated
    def get(self):
        param = json.loads(self.get_argument('base'))
        sub_param = param['param']
        user_email_id = int(self.get_param('id', sub_param))

        user = self.current_user
        uid = user['uid']

        user_email = email_controller.get_one_user_mail_by_id(user_email_id)
        if not user_email:
            self.return_error(PARAM_ERROR)

        # 获取全部邮件信息
        email_info = email_controller.get_all_email_info()
        new_email_info = {}
        for item in email_info:
            new_email_info[item['id']] = item

        # 判断是否符合条件的邮件
        if int(user_email['is_read']) != 9 and diff_days(int(user_email['send_date'])) < 30:
            # 判断此邮件是否有奖励
            if new_email_info[user_email['eid']]['reward_id']:
                reward_id = new_email_info[user_email['eid']]['reward_id']

                # 获取奖励详情
                reward_list = reward_controller.get_all_reward_info()
                new_reward_list = {}
                for reward in reward_list:
                    new_reward_list[reward['id']] = reward

                # 获取道具详情
                prop_list = prop_controller.get_all_prop_info()
                new_prop_list = {}
                for prop in prop_list:
                    new_prop_list[prop['id']] = prop

                # 领取奖励
                for rid in reward_id.split(','):
                    rid = int(rid)
                    # prop_id 1: 金币
                    if int(new_prop_list[new_reward_list[rid]['prop_id']]['id']) == 1:
                        # 奖励金币数量
                        reward_quantity = new_reward_list[rid]['reward_quantity']

                        # 当前玩家金币总数
                        money = user[0]['money']

                        # 领取奖励后，玩家金币总数
                        total = int(reward_quantity) + int(money)

                        login_hall_controller.update_user_in_cache(uid, {'money': total})

                # 删除邮件
                if email_controller.update_user_mail_by_id(user_email_id, {'is_read': 9}):
                    self.return_success([{'money': total}])

            else:
                # 删除邮件
                if email_controller.update_user_mail_by_id(user_email_id, {'is_read': 9}):
                    self.return_success([])

        else:
            self.return_error(PARAM_ERROR)

    def post(self):
        pass

