# coding=utf-8

__author__ = 'jamon'

from share.timer_task import TimerTask

from service.mahjong.constants.gamedefine import TimerType
from service.mahjong.models.callbackmanager import CallbackManager
from obespoir.share.ob_log import logger

import time


class TimerManager(object):
    """
    定时器
    """
    def __init__(self):
        self.timer_dict = {}

    @classmethod
    def call_later(cls, interval, callback_func, *args, **kwargs):
        return TimerTask.call_later(interval, callback_func, *args, **kwargs)

    def tmhash(self, desk_id, timer_id):
        return "%s_%s" % (str(desk_id), str(timer_id))

    def get_timer(self, desk_id, seat_id):
        tid = self.tmhash(desk_id, seat_id)
        return self.timer_dict.get(tid, None)

    def add_timer(self, desk_id, seat_id, interval, t_type=TimerType.NORMAL, call_type=None, call_params={}):
        """
        添加定时任务
        :param desk_id:
        :param seat_id:
        :param interval:
        :param call_type:
        :param args:
        :param kwargs:
        :return:
        """
        logger.debug(u"add_timer: %s", str([desk_id, seat_id, interval, t_type, call_type, call_params]))
        tid = self.tmhash(desk_id, seat_id)
        t_task = self.timer_dict.get(tid, None)
        print("add_timer", tid, t_task)
        if t_task is not None:
            self.kill_timer(desk_id, seat_id)

        self.timer_dict[tid] = {
            "type": t_type, "end_time": time.time()+interval, "call_type": call_type, "params": call_params,
            "call": self.call_later(interval, self.execute, desk_id, seat_id, call_type, call_params)
        }

        return 1

    def execute(self, desk_id, seat_id, call_type, call_params):
        tid = self.tmhash(desk_id, seat_id)
        if not self.timer_dict.get(tid, None):
            return
        self.kill_timer(desk_id, seat_id, is_force=True)
        logger.debug(u"kill_timer:%s", str([desk_id, seat_id, call_type, call_params]))
        return CallbackManager.get_instance(desk_id).execute(call_type, call_params)

    def kill_timer(self, desk_id, seat_id, is_force=True):
        tid = self.tmhash(desk_id, seat_id)
        t_task = self.timer_dict.get(tid, None)
        if t_task and (TimerType.NORMAL == t_task.get("type", TimerType.NORMAL) or is_force):
            # 如果当前任务存在并且还在执行
            print("t_task call= ", t_task["call"])
            # if t_task["call"] and t_task["call"].active():
            if t_task["call"]:
                # if t_task["call"].active():
                if not t_task["call"].done():
                    t_task["call"].cancel()
                del self.timer_dict[tid]
            else:
                print("killllllllllllllllllllll:", self.timer_dict)
        return 1


timer_manager_ins = TimerManager()