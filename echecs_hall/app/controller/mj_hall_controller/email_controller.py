#!/usr/bin/env python
# coding=utf-8
from app.data_bridge import mj_hall_bridge


def validate_user_mail(uid):
    """
    用户邮件是否存在mysql table中
    :param: uid
    :return:bool
    """
    # TODO 查看是否存在redis中
    return mj_hall_bridge.validate_user_mail_in_table(uid)


def get_user_mail_by_uid(uid):
    """
    通过用户id获取用户邮件
    :param: uid
    :return:list
    """
    # TODO 获取用户邮件
    return mj_hall_bridge.get_user_mail_by_uid(uid)


def get_one_user_mail_by_id(id):
    """
    通过id获取指定用户邮件
    :param: uid
    :return:list
    """
    # TODO 获取指定用户邮件
    return mj_hall_bridge.get_one_user_mail_by_id(id)


def update_user_mail_by_id(id, data):
    """
    通过id修改用户邮件
    :param: uid
    :return:
    """
    # TODO 修改用户邮件
    return mj_hall_bridge.update_user_mail_by_id(id, data)


def get_email_info_by_id(id):
    """
    通过用户id获取邮件详情
    :param: uid
    :return:dict
    """
    # TODO 获取邮件详情
    return mj_hall_bridge.get_email_info_by_id(id)


def get_all_email_info():
    """
    获取邮件详情
    :param:
    :return:list
    """
    return mj_hall_bridge.get_all_email_info()






