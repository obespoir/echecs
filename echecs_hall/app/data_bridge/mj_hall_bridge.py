#!/usr/bin/env python
# coding=utf-8

from app.extensions.redis.redis_utils import redis_db
from app.extensions.redis.redis_operation import set_multi_hash_in_redis
from app.extensions.redis.redis_operation import set_single_hash_in_redis
from app.extensions.redis.redis_operation import update_single_hash_in_redis
from app.extensions.redis.redis_operation import get_all_in_redis, get_one_in_redis
from app.models.user import User
from app.models.user_info import UserInfo
from app.models.match_game import MatchGame
from app.models.game_rule import GameRule
from app.models.user_mail import UserMail
from app.models.email_info import EmailInfo
from app.models.good_info import GoodInfo
from app.models.reward_info import RewardInfo
from app.models.prop_info import PropInfo
from app.models.income_support import IncomeSupport


def check_user_is_exist(username):
    return User.check_user_is_exist(username)


def get_user_info_by_username(username):
    return User.get_user_info_by_username(username)


def validate_password(username, password):
    return User.validate_password(username, password)


def get_user_info_in_cache(uid):
    r_key = 'hu:' + str(uid)
    return get_one_in_redis(r_key)


def save_user_info_in_cache(uid, user_info):
    r_key = 'hu:' + str(uid)
    return set_single_hash_in_redis({r_key: user_info})


def update_user_in_cache(uid, user_info):
    r_key = 'hu:' + str(uid)
    return update_single_hash_in_redis({r_key: user_info})


def get_match_data_in_cache(uid):
    r_key = 'hu:' + str(uid) + ':match'
    return get_one_in_redis(r_key)


def get_match_data_by_uid(uid):
    return MatchGame.get_user_match_data_by_uid(uid)


def save_match_data_in_cache(uid, match_data):
    r_key = 'hu:' + str(uid) + ':match'
    return set_single_hash_in_redis({r_key: match_data})


def get_game_rule_in_cache(uid):
    r_key = 'hu:' + str(uid) + ':rule'
    return get_one_in_redis(r_key)


def get_game_rule_by_uid(uid):
    return GameRule.get_user_game_rule_by_uid(uid)


def save_game_rule_in_cache(uid, game_rule):
    r_key = 'hu:' + str(uid) + ':rule'
    return set_single_hash_in_redis({r_key: game_rule})


def validate_user_mail_in_table(uid):
    return UserMail.validate_user_mail_in_table(uid)


def get_user_mail_by_uid(uid):
    return UserMail.get_user_mail_by_uid(uid)


def get_one_user_mail_by_id(id):
    return UserMail.get_one_user_mail_by_id(id)


def update_user_mail_by_id(id, data):
    return UserMail.update_user_mail_by_id(id, data)


def get_email_info_by_id(id):
    return EmailInfo.get_email_info_by_id(id)


def get_all_email_info():
    return EmailInfo.get_all_email_info()


def get_all_good_info():
    return GoodInfo.get_all_good_info()


def get_good_info_by_id(id):
    return GoodInfo.get_good_info_by_id(id)


def get_all_reward_info():
    return RewardInfo.get_all_reward_info()


def get_all_prop_info():
    return PropInfo.get_all_prop_info()


def get_income_support_by_uid(uid):
    return IncomeSupport.get_income_support_by_uid(uid)


def save_income_support(data):
    return IncomeSupport.add(data)


def update_income_support_by_id(id, data):
    return IncomeSupport.update_income_support_by_id(id, data)


def save_user(data):
    return User.add(data)


def save_user_info(data):
    return UserInfo.add(data)


def get_user_info_by_id(id):
    return User.get_info_by_uid(id)
