# coding=utf-8
import os
from app.extensions.config_parser import ConfigParser

"""
全局变量储存地点
"""

class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kw)
        return cls._instance


class Config(object):
    __metaclass__ = Singleton  # 注意：本套代码是在单进程下运行，否则会引发线程安全问题

    def __init__(self):
        self.config_path = "config.json"


class GlobalObject(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.db = None
        self.redis_db = None
        self.settings = None  # 用于储存配置文件相关信息
        self.elementary_room = {}  # 用于储存出机场人数
        self.intermediate_room = {}  # 中级场
        self.top_room = {}  # 高级场
        self.room_cfg_list = None  # 所有房间配置
        self.income_support = 4000  # 破产补助
        self.init_settings()


    def init_settings(self):
        path = os.getcwd()+"/config.ini"
        settings = ConfigParser(path)
        self.settings = settings




settings = ConfigParser(os.getcwd() + "/config.ini")
print("globalobject settings = ", settings)