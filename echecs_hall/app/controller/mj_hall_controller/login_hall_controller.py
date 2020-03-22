#!/usr/bin/env python
# coding=utf-8

from app.data_bridge import mj_hall_bridge


def check_user_is_exist(username):
    return mj_hall_bridge.check_user_is_exist(username)


def get_user_info_by_username(username):
    return mj_hall_bridge.get_user_info_by_username(username)


def validate_password(username, password):
    return mj_hall_bridge.validate_password(username, password)


def get_user_info_in_cache(uid):
    return mj_hall_bridge.get_user_info_in_cache(uid)


def save_user_info_in_cache(uid, user_info):
    return mj_hall_bridge.save_user_info_in_cache(uid, user_info)


def save_user(user):
    return mj_hall_bridge.save_user(user)


def save_user_info(user_info):
    return mj_hall_bridge.save_user_info(user_info)


def get_match_data_in_cache(uid):
    """
    通过用户id获取redis匹配场数据
    :param: uid
    :return:list
    """
    # TODO 获取匹配场数据
    return mj_hall_bridge.get_match_data_in_cache(uid)


def get_match_data_by_uid(uid):
    """
    通过用户id获取mysql匹配场数据
    :param: uid
    :return:dict
    """
# TODO 获取匹配场数据
    return mj_hall_bridge.get_match_data_by_uid(uid)


def save_match_data_in_cache(uid, match_data):
    """
    把mysql用户匹配场数据存入redis
    :param: uid, match_data
    :return:bool
    """
    # TODO 存redis中
    return mj_hall_bridge.save_match_data_in_cache(uid, match_data)


def get_game_rule_in_cache(uid):
    return mj_hall_bridge.get_game_rule_in_cache(uid)


def get_game_rule_by_uid(uid):
    """
    通过用户id获取规则数据
    :param: uid
    :return:dict
    """
    # TODO 获取匹配场数据
    return mj_hall_bridge.get_game_rule_by_uid(uid)


def save_game_rule_in_cache(uid, game_rule):
    """
    把mysql用户规则数据存入redis
    :param: uid, game_rule
    :return:bool
    """
    # TODO 存redis中
    return mj_hall_bridge.save_game_rule_in_cache(uid, game_rule)


def update_user_in_cache(uid, user_info):
    """
    把mysql用户数据更新redis
    :param: uid, dict
    :return:bool
    """
    # TODO 存入redis中
    return mj_hall_bridge.update_user_in_cache(uid, user_info)


