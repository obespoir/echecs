# coding=utf-8

import os
from service.mahjong.models.config.parse_config import parse_config_ins


class InitConfig(object):
    """
    游戏预配置文件解析
    """
    def __init__(self):
        self.all_config = {}
        self.init_from_file()

    def init_from_file(self):
        self.all_config["default"] = parse_config_ins.parse("../game_setting/default.json")
        files = os.listdir("../game_setting/special")
        for f in files:
            name = f.split('.')[0]
            self.all_config[name] = parse_config_ins.parse("../game_setting/special/" + f)

    @property
    def default_config(self):
        return self.all_config.get("default", {})


init_config_ins = InitConfig()
init_config_ins.init_from_file()

