# coding=utf-8
from app.data_bridge import mj_hall_bridge


def get_income_support_by_uid(uid):
    return mj_hall_bridge.get_income_support_by_uid(uid)


def save_income_support(data):
    return mj_hall_bridge.save_income_support(data)


def update_income_support_by_id(id, data):
    return mj_hall_bridge.update_income_support_by_id(id, data)